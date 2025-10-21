"""
Türkçe yardımcı fonksiyonlar: NPM Top-N listesi, bağımlılıkların çekilmesi,
yönlü ağın (Dependent → Dependency) kurulması, merkeziyet metrikleri ve çıktıların kaydı.

Bu modül, analysis.ipynb tarafından kullanılır.
"""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Dict, List, Set, Tuple

import networkx as nx
import requests
from requests.utils import quote


# NPM ve üçüncü taraf uç noktaları
ECOSYSTEMS_PACKAGE_NAMES_URL = (
    "https://packages.ecosyste.ms/api/v1/registries/npmjs.org/package_names"
)
NPMS_SEARCH_URL = "https://api.npms.io/v2/search"
NPM_SEARCH_URL = "https://registry.npmjs.org/-/v1/search"
NPM_REGISTRY_BASE = "https://registry.npmjs.org"


# Bir dosyadan satır bazlı paket adı listesi oku
def read_list(path: Path) -> List[str]:
    """Bir dosyadan paket isimlerini (satır başına bir isim) oku ve liste döndür."""
    if not path.exists():
        return []
    return [
        line.strip()
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


# ecosyste.ms üzerinden tek sayfada (<=1000) Top-N paket adlarını çek
def _fetch_top_packages_ecosystems(limit: int) -> List[str]:
    """ecosyste.ms paket adlarını tek sayfa (<=1000) şeklinde, indirmeye göre sırayla çek."""
    per_page = min(max(limit, 1), 1000)
    params = {"per_page": per_page, "sort": "downloads", "page": 1}
    resp = requests.get(ECOSYSTEMS_PACKAGE_NAMES_URL, params=params, timeout=60)
    resp.raise_for_status()
    names: List[str] = resp.json()
    return names[:limit]


# ecosyste.ms üzerinden sayfalayarak (per_page=1000) Top-N paket adlarını topla
def _fetch_top_packages_ecosystems_paginated(limit: int) -> List[str]:
    """ecosyste.ms üzerinden sayfalayarak limit adede kadar paket adı topla (per_page=1000)."""
    collected: List[str] = []
    per_page = 1000
    page = 1
    while len(collected) < limit:
        params = {"per_page": per_page, "sort": "downloads", "page": page}
        resp = requests.get(ECOSYSTEMS_PACKAGE_NAMES_URL, params=params, timeout=60)
        if resp.status_code != 200:
            break
        batch = resp.json()
        if not isinstance(batch, list) or not batch:
            break
        collected.extend(batch)
        page += 1
        if len(batch) < per_page:
            break
    # Sıra korunarak tekilleştir
    seen: Set[str] = set()
    deduped: List[str] = []
    for name in collected:
        if name and name not in seen:
            seen.add(name)
            deduped.append(name)
        if len(deduped) >= limit:
            break
    return deduped


# npms.io popülerlik skoruna göre yaklaşık Top-N paket adlarını çek (yedek)
def _fetch_top_packages_npms(limit: int) -> List[str]:
    """npms.io popülerlik skorunu yaklaşık olarak kullanarak isim listesi çek."""
    params = {"q": "scope:public", "size": min(limit, 250)}
    resp = requests.get(NPMS_SEARCH_URL, params=params, timeout=60)
    resp.raise_for_status()
    data = resp.json()
    results = data.get("results", [])
    results.sort(
        key=lambda r: (r.get("score", {}).get("detail", {}).get("popularity", 0.0)),
        reverse=True,
    )
    names = [r.get("package", {}).get("name") for r in results if r.get("package")]
    return [n for n in names if n][:limit]


# Top-N paket adlarını getir (öncelik ecosyste.ms; npm search/npms.io yedek)
def fetch_top_packages(limit: int = 100) -> List[str]:
    """En çok indirilen Top-N paket adlarını getir (tercihen ecosyste.ms, ardından yedekler)."""
    try:
        if limit > 1000:
            names = _fetch_top_packages_ecosystems_paginated(limit)
            if names:
                return names
        names = _fetch_top_packages_ecosystems(limit)
        if names:
            return names
    except Exception:
        pass
    # npm registry araması (popularity) yedeği
    try:
        params = {
            "text": "*",
            "size": min(limit, 250),
            "from": 0,
            "quality": 0.0,
            "popularity": 1.0,
            "maintenance": 0.0,
        }
        resp = requests.get(NPM_SEARCH_URL, params=params, timeout=60)
        resp.raise_for_status()
        data = resp.json()
        objects = data.get("objects", [])
        names = [o.get("package", {}).get("name") for o in objects]
        names = [n for n in names if n]
        if names:
            return names[:limit]
    except Exception:
        pass
    # Son yedek: npms.io
    return _fetch_top_packages_npms(limit)


# NPM paket adını URL için güvenli biçimde kodla (scoped paketler dahil)
def encode_npm_name(name: str) -> str:
    """NPM paket adını URL yolunda güvenli kullanmak için kodla (scoped paketlerde '/' da kodlanır)."""
    return quote(name, safe="")


# Bir paketin en güncel sürümünden dependencies alanını çek
def fetch_dependencies(package: str) -> Dict[str, str]:
    """Bir paketin npm registry’deki en güncel sürümünden `dependencies` alanını çek."""
    encoded = encode_npm_name(package)
    url = f"{NPM_REGISTRY_BASE}/{encoded}"
    resp = requests.get(url, timeout=60)
    if resp.status_code != 200:
        return {}
    data = resp.json()

    latest = (data.get("dist-tags") or {}).get("latest") if isinstance(data, dict) else None
    versions = data.get("versions", {}) if isinstance(data, dict) else {}
    version_obj = None
    if latest and latest in versions:
        version_obj = versions.get(latest, {})
    elif versions:
        try:
            version_key = sorted(versions.keys())[-1]
            version_obj = versions.get(version_key, {})
        except Exception:
            version_obj = {}
    else:
        version_obj = {}

    deps = version_obj.get("dependencies", {}) if isinstance(version_obj, dict) else {}
    return deps if isinstance(deps, dict) else {}


# Top-N listesinden yönlü bağımlılık ağı kur (Dependent → Dependency)
def build_dependency_graph(top_packages: List[str]) -> Tuple[nx.DiGraph, Set[str]]:
    """Top-N listesi için yönlü bir bağımlılık ağı (Dependent → Dependency) kur ve döndür."""
    G = nx.DiGraph()
    top_set: Set[str] = set(top_packages)
    for pkg in top_packages:
        G.add_node(pkg)
    for pkg in top_packages:
        deps = fetch_dependencies(pkg)
        for dep in deps.keys():
            G.add_edge(pkg, dep)  # Dependent → Dependency
            if dep not in G:
                G.add_node(dep)
    return G, top_set


# Ağ için in-degree, out-degree ve betweenness metriklerini hesapla
def compute_metrics(G: nx.DiGraph) -> Tuple[Dict[str, int], Dict[str, int], Dict[str, float]]:
    """Ağ için in-degree, out-degree ve betweenness merkeziyet metriklerini hesapla."""
    in_deg: Dict[str, int] = dict(G.in_degree())
    out_deg: Dict[str, int] = dict(G.out_degree())
    btw: Dict[str, float] = nx.betweenness_centrality(G, normalized=True)
    return in_deg, out_deg, btw


# Kenar listesini CSV olarak kaydet (source=dependent, target=dependency)
def save_edges(G: nx.DiGraph, out_path: Path) -> None:
    """Kenar listesini CSV olarak kaydet (source=dependent, target=dependency)."""
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["source", "target"])
        for u, v in G.edges():
            w.writerow([u, v])


# Düğüm metriklerini CSV olarak kaydet (in_degree, out_degree, betweenness)
def save_metrics(
    in_deg: Dict[str, int],
    out_deg: Dict[str, int],
    btw: Dict[str, float],
    top_set: Set[str],
    out_path: Path,
) -> None:
    """Düğüm metriklerini CSV olarak kaydet (paket, in_degree, out_degree, betweenness, is_top100)."""
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["package", "in_degree", "out_degree", "betweenness", "is_top100"])
        all_nodes = set(in_deg.keys()) | set(out_deg.keys()) | set(btw.keys())
        for n in sorted(all_nodes):
            w.writerow([
                n,
                in_deg.get(n, 0),
                out_deg.get(n, 0),
                f"{btw.get(n, 0.0):.6f}",
                str(n in top_set),
            ])


# Kısa bir Markdown raporu üret (in/out/between için ilk 20 listeler)
def save_report(
    in_deg: Dict[str, int], out_deg: Dict[str, int], btw: Dict[str, float], top_set: Set[str], out_path: Path
) -> None:
    """Kısa bir Markdown raporu üret ve kaydet (in-degree/out-degree/betweenness için ilk 20 listeler)."""
    out_path.parent.mkdir(parents=True, exist_ok=True)
    top_in_all = sorted(in_deg.items(), key=lambda kv: kv[1], reverse=True)[:20]
    top_out_all = sorted(out_deg.items(), key=lambda kv: kv[1], reverse=True)[:20]
    top_btw_all = sorted(btw.items(), key=lambda kv: kv[1], reverse=True)[:20]
    top_in_top = sorted(
        ((n, in_deg.get(n, 0)) for n in top_set), key=lambda kv: kv[1], reverse=True
    )[:20]
    top_out_top = sorted(
        ((n, out_deg.get(n, 0)) for n in top_set), key=lambda kv: kv[1], reverse=True
    )[:20]
    top_btw_top = sorted(
        ((n, btw.get(n, 0.0)) for n in top_set), key=lambda kv: kv[1], reverse=True
    )[:20]

    lines: List[str] = []
    lines.append("# NPM Bağımlılık Ağı Raporu")
    lines.append("")
    lines.append("## In-Degree İlk 20 (Tüm Düğümler)")
    for n, v in top_in_all:
        lines.append(f"- {n}: {v}")
    lines.append("")
    lines.append("## Out-Degree İlk 20 (Tüm Düğümler)")
    for n, v in top_out_all:
        lines.append(f"- {n}: {v}")
    lines.append("")
    lines.append("## Betweenness İlk 20 (Tüm Düğümler)")
    for n, v in top_btw_all:
        lines.append(f"- {n}: {v:.6f}")
    lines.append("")
    lines.append("## In-Degree İlk 20 (Top 200 Kohortu)")
    for n, v in top_in_top:
        lines.append(f"- {n}: {v}")
    lines.append("")
    lines.append("## Out-Degree İlk 20 (Top 200 Kohortu)")
    for n, v in top_out_top:
        lines.append(f"- {n}: {v}")
    lines.append("")
    lines.append("## Betweenness İlk 20 (Top 200 Kohortu)")
    for n, v in top_btw_top:
        lines.append(f"- {n}: {v:.6f}")

    out_path.write_text("\n".join(lines), encoding="utf-8")
