"""
Yardımcı fonksiyonlar (TR)

- Top N paket listesini çek (ecosyste.ms öncelikli; npm search / npms.io yedek).
- En güncel sürümden bağımlılıkları çek.
- Yönü Dependent -> Dependency olan yönlü ağ kur.
- Merkeziyet metriklerini (in/out-degree, betweenness) hesapla.
- Basit disk önbelleği ve tekrar denemeleri içerir.
- CSV / JSON çıktı yardımcıları ve (opsiyonel) grafik üreticiler barındırır.

Not: Bu modül `analysis/analysis.ipynb` tarafından kullanılmak üzere tasarlanmıştır.
"""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional

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


# ecosyste.ms üzerinden tek sayfada (<=1000) Top N paket adlarını çek
def _fetch_top_packages_ecosystems(limit: int) -> List[str]:
    """ecosyste.ms paket adlarını tek sayfa (<=1000) olarak, indirmeye göre sıralayarak çek."""
    per_page = min(max(limit, 1), 1000)
    params = {"per_page": per_page, "sort": "downloads", "page": 1}
    resp = requests.get(ECOSYSTEMS_PACKAGE_NAMES_URL, params=params, timeout=60)
    resp.raise_for_status()
    names: List[str] = resp.json()
    return names[:limit]


# ecosyste.ms üzerinden sayfalayarak (per_page=1000) Top N paket adlarını topla
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


# npms.io popülerlik skoruna göre yaklaşık Top N paket adlarını çek (yedek)
def _fetch_top_packages_npms(limit: int) -> List[str]:
    """npms.io popülerlik skorunu yaklaşık olarak kullanarak isim listesi çek."""
    # Basit arama: popüler bir tohum (react) ile başlayıp sonuçları al
    params = {"q": "react", "size": min(limit, 250)}
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


def _fetch_top_packages_npm_search_aggregate(limit: int) -> List[str]:
    """NPM search API ile birden çok sorgu 'tohumu' kullanarak popüler paketleri topla (TR).

    Tek bir wildcard sorgusu 400 döndürebildiği için, farklı tohum metinleri
    (harfler ve popüler anahtarlar) ile birleştirerek daha geniş kapsama ulaşır.
    Sonuçlar popularity detayıyla sıralanır ve tekilleştirilir.
    """
    base = NPM_SEARCH_URL
    seeds = [
        "react",
        "a",
        "e",
        "i",
        "o",
        "u",
        "s",
        "t",
        "n",
        "l",
        "c",
        "r",
    ]
    best: Dict[str, float] = {}
    max_pages = 5  # her seed için en fazla 5 sayfa (5*250=1250)
    for seed in seeds:
        for page in range(max_pages):
            params = {
                "text": seed,
                "size": 250,
                "from": page * 250,
                "quality": 0.0,
                "popularity": 1.0,
                "maintenance": 0.0,
            }
            try:
                resp = requests.get(base, params=params, timeout=60)
                if resp.status_code != 200:
                    break
                data = resp.json()
                objects = data.get("objects", [])
                if not objects:
                    break
                for o in objects:
                    pkg = (o.get("package", {}) or {}).get("name")
                    pop = (
                        (o.get("score", {}) or {})
                        .get("detail", {})
                        .get("popularity", 0.0)
                    )
                    if pkg:
                        # en yüksek popülerlik değerini tut
                        if pop is None:
                            pop = 0.0
                        if (pkg not in best) or (pop > best[pkg]):
                            best[pkg] = float(pop)
                # yeterli veri toplandıysa erken çık
                if len(best) >= max(limit * 2, 500):
                    break
            except Exception:
                break
        if len(best) >= max(limit * 2, 500):
            break

    ranked = sorted(best.items(), key=lambda kv: kv[1], reverse=True)
    names = [k for k, _ in ranked]
    return names[:limit]


# Top N paket adlarını getir (öncelik ecosyste.ms; npm search / npms.io yedek)
def fetch_top_packages(limit: int = 100) -> List[str]:
    """En çok indirilen Top N paket adlarını getir (tercihen ecosyste.ms, ardından yedekler)."""
    try:
        # 1000 ve üzeri için sayfalı toplama daha güvenilir
        if limit >= 1000:
            names = _fetch_top_packages_ecosystems_paginated(limit)
            if names:
                return names
        names = _fetch_top_packages_ecosystems(limit)
        if names:
            return names
    except Exception:
        pass
    # npm registry araması (popularity) yedeği — çoklu tohum ile birleştir
    try:
        names = _fetch_top_packages_npm_search_aggregate(limit)
        if names:
            return names
    except Exception:
        pass
    # Son yedek: npms.io (basit popüler arama)
    return _fetch_top_packages_npms(limit)


# NPM paket adını URL için güvenli biçimde kodla (scoped paketler dahil)
def encode_npm_name(name: str) -> str:
    """NPM paket adını URL yolunda güvenli kullanmak için kodla (scoped paketlerde '/' da kodlanır)."""
    return quote(name, safe="")


# Bir paketin en güncel sürümünden dependencies alanını çek
def fetch_dependencies(
    package: str,
    session: Optional[requests.Session] = None,
    include_peer: bool = False,
) -> Dict[str, str]:
    """Paketin npm registry'deki en güncel sürümünden `dependencies` alanını çek.

    Daha verimli olmak için paylaşılan bir `requests.Session` (varsa) kullanır.
    """
    encoded = encode_npm_name(package)
    url = f"{NPM_REGISTRY_BASE}/{encoded}"
    http = session if session is not None else requests
    resp = http.get(url, timeout=60)
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
    if include_peer:
        peer = version_obj.get("peerDependencies", {}) if isinstance(version_obj, dict) else {}
        if isinstance(peer, dict):
            # Birleşim (key set); aynı anahtar varsa dependencies öncelikli
            deps = dict({**peer, **(deps if isinstance(deps, dict) else {})})
    return deps if isinstance(deps, dict) else {}


# Basit disk önbelleği (JSON) — bağımlılık sorguları için
def _load_cache(path: Path) -> Dict[str, Dict[str, str]]:
    """Önbelleği yükle (yoksa boş sözlük)."""
    try:
        if path.exists():
            import json
            return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        pass
    return {}


def _save_cache(path: Path, cache: Dict[str, Dict[str, str]]) -> None:
    """Önbelleği diske yaz (güvenli yazım)."""
    try:
        import json, tempfile
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp = Path(tempfile.gettempdir()) / (path.name + ".tmp")
        tmp.write_text(json.dumps(cache, ensure_ascii=False), encoding="utf-8")
        tmp.replace(path)
    except Exception:
        pass


# Top N listesinden yönlü bağımlılık ağı kur (Dependent -> Dependency)
def build_dependency_graph(
    top_packages: List[str],
    cache_path: Optional[Path] = None,
    include_peer_deps: bool = False,
) -> Tuple[nx.DiGraph, Set[str]]:
    """Top N listesi için yönlü bir bağımlılık ağı (Dependent -> Dependency) kur ve döndür.

    Bağlantı maliyetini azaltmak için tek bir HTTP oturumu (Session) yeniden kullanılır.
    """
    G = nx.DiGraph()
    top_set: Set[str] = set(top_packages)
    for pkg in top_packages:
        G.add_node(pkg)
    if cache_path is None:
        cache_path = Path("results/cache_deps.json")
    cache = _load_cache(cache_path)
    with requests.Session() as session:
        for pkg in top_packages:
            # Önbelleğin kullanılması
            if pkg in cache:
                deps: Dict[str, str] = cache.get(pkg) or {}
            else:
                # Basit 3 denemeli çekim
                deps = {}
                for _ in range(3):
                    deps = fetch_dependencies(pkg, session=session, include_peer=include_peer_deps)
                    if deps:
                        break
                cache[pkg] = deps
            for dep in deps.keys():
                # NetworkX add_edge eksik düğümleri otomatik ekler
                G.add_edge(pkg, dep)  # Dependent -> Dependency
    _save_cache(cache_path, cache)
    return G, top_set


# Ağ için in-degree, out-degree ve betweenness metriklerini hesapla
def compute_metrics(
    G: nx.DiGraph, sample_k: Optional[int] = None
) -> Tuple[Dict[str, int], Dict[str, int], Dict[str, float]]:
    """Ağ için in-degree, out-degree ve betweenness merkeziyet metriklerini hesapla.

    Büyük graflarda (ör. >1200 düğüm) betweenness için örnekleme (k)
    kullanarak hesabı hızlandırır. sample_k verilirse o değer esas alınır.
    """
    in_deg: Dict[str, int] = dict(G.in_degree())
    out_deg: Dict[str, int] = dict(G.out_degree())
    n = G.number_of_nodes()
    if sample_k is not None:
        k = min(sample_k, n)
        btw = nx.betweenness_centrality(G, k=k, normalized=True, seed=42)
    elif n > 1200:
        k = min(200, n)
        btw = nx.betweenness_centrality(G, k=k, normalized=True, seed=42)
    else:
        btw = nx.betweenness_centrality(G, normalized=True)
    return in_deg, out_deg, btw


# --- Risk skoru (bileşik) ---
def _minmax_norm(values: Dict[str, float]) -> Dict[str, float]:
    """Min–max normalize et (tüm değerler aynıysa 0 döndür)."""
    if not values:
        return {}
    vmin = min(values.values())
    vmax = max(values.values())
    if vmax <= vmin:
        return {k: 0.0 for k in values}
    return {k: (v - vmin) / (vmax - vmin) for k, v in values.items()}


def compute_risk_scores(
    in_deg: Dict[str, int],
    out_deg: Dict[str, int],
    btw: Dict[str, float],
    w_in: float = 0.5,
    w_out: float = 0.2,
    w_btw: float = 0.3,
) -> Dict[str, float]:
    """Normalize (min–max) edilmiş in/out/between ile bileşik risk skoru hesapla."""
    # float dönüştürme
    in_f = {k: float(v) for k, v in in_deg.items()}
    out_f = {k: float(v) for k, v in out_deg.items()}
    in_n = _minmax_norm(in_f)
    out_n = _minmax_norm(out_f)
    btw_n = _minmax_norm(btw)
    nodes = set(in_deg) | set(out_deg) | set(btw)
    scores: Dict[str, float] = {}
    for n in nodes:
        scores[n] = w_in * in_n.get(n, 0.0) + w_out * out_n.get(n, 0.0) + w_btw * btw_n.get(n, 0.0)
    return scores


def save_risk_scores(
    risk: Dict[str, float],
    in_deg: Dict[str, int],
    out_deg: Dict[str, int],
    btw: Dict[str, float],
    top_set: Set[str],
    out_path: Path,
) -> None:
    """Risk skorlarını CSV olarak kaydet (paket, risk, in, out, between, is_topN)."""
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["package", "risk_score", "in_degree", "out_degree", "betweenness", "is_topN"])
        for n, r in sorted(risk.items(), key=lambda kv: kv[1], reverse=True):
            w.writerow([n, f"{r:.6f}", in_deg.get(n, 0), out_deg.get(n, 0), f"{btw.get(n, 0.0):.6f}", str(n in top_set)])


# --- Robustluk analizi ---
def robustness_remove_and_stats(
    G: nx.DiGraph,
    remove_nodes: List[str],
) -> Dict[str, float]:
    """Belirtilen düğümler kaldırıldıktan sonra bağlanırlık istatistikleri (zayıf)."""
    H = G.copy()
    H.remove_nodes_from(remove_nodes)
    W = H.to_undirected()
    comps = list(nx.connected_components(W))
    comp_sizes = sorted([len(c) for c in comps], reverse=True)
    largest = comp_sizes[0] if comp_sizes else 0
    stats = {
        "nodes": float(H.number_of_nodes()),
        "edges": float(H.number_of_edges()),
        "components_count": float(len(comps)),
        "largest_component_size": float(largest),
    }
    # En büyük bileşen için çap (diameter) hesaplamayı dene
    try:
        if comps:
            giant = W.subgraph(max(comps, key=len)).copy()
            stats["diameter_lcc"] = float(nx.diameter(giant)) if nx.is_connected(giant) else float("nan")
        else:
            stats["diameter_lcc"] = float("nan")
    except Exception:
        stats["diameter_lcc"] = float("nan")
    return stats


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
    """Düğüm metriklerini CSV olarak kaydet (paket, in_degree, out_degree, betweenness, is_topN)."""
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["package", "in_degree", "out_degree", "betweenness", "is_topN"])
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
    """Kısa bir Markdown raporu üret ve kaydet (in/out/between için ilk 20 listeler)."""
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
    lines.append("## In-Degree İlk 20 (Top N Kohortu)")
    for n, v in top_in_top:
        lines.append(f"- {n}: {v}")
    lines.append("")
    lines.append("## Out-Degree İlk 20 (Top N Kohortu)")
    for n, v in top_out_top:
        lines.append(f"- {n}: {v}")
    lines.append("")
    lines.append("## Betweenness İlk 20 (Top N Kohortu)")
    for n, v in top_btw_top:
        lines.append(f"- {n}: {v:.6f}")

    out_path.write_text("\n".join(lines), encoding="utf-8")


# Genel grafik istatistiklerini JSON olarak kaydet
def save_graph_stats(G: nx.DiGraph, out_path: Path) -> None:
    """Düğüm/kenar sayısı ve zayıf bileşen istatistiklerini JSON olarak kaydet."""
    import json
    W = G.to_undirected()
    comps = list(nx.connected_components(W))
    comp_sizes = sorted([len(c) for c in comps], reverse=True)
    stats = {
        "nodes": int(G.number_of_nodes()),
        "edges": int(G.number_of_edges()),
        "components_count": int(len(comps)),
        "largest_component_size": int(comp_sizes[0]) if comp_sizes else 0,
    }
    try:
        if comps:
            giant = W.subgraph(max(comps, key=len)).copy()
            stats["diameter_lcc"] = float(nx.diameter(giant)) if nx.is_connected(giant) else float("nan")
        else:
            stats["diameter_lcc"] = float("nan")
    except Exception:
        stats["diameter_lcc"] = float("nan")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(stats, ensure_ascii=False, indent=2), encoding="utf-8")


# Belirli tohum düğümler için ters yönde (dependents) yayılım etki boyutu
def cascade_impact_counts(G: nx.DiGraph, seeds: List[str]) -> Dict[str, int]:
    """Her seed için, ters yön (dependents) boyunca erişilebilen düğüm sayısını hesapla.

    Kenarlar Dependent->Dependency yönündedir. Bir bağımlılığın ele geçirilmesi,
    orijinal grafikte bu düğüme ulaşabilen (yani dependents) düğümleri etkiler.
    Bu nedenle G'nin tersinde, seed'den erişilebilen düğümler sayılır.
    """
    G_rev = G.reverse(copy=False)
    from collections import deque
    result: Dict[str, int] = {}
    for s in seeds:
        if s not in G_rev:
            result[s] = 0
            continue
        seen = {s}
        dq = deque([s])
        while dq:
            u = dq.popleft()
            for v in G_rev.successors(u):
                if v not in seen:
                    seen.add(v)
                    dq.append(v)
        # Kendisi hariç
        result[s] = max(0, len(seen) - 1)
    return result


def save_cascade_impact(impact: Dict[str, int], out_path: Path) -> None:
    """Kaskad etki sayaçlarını CSV olarak kaydet (seed, impacted_count)."""
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["package", "impacted_count"])
        for n, c in sorted(impact.items(), key=lambda kv: kv[1], reverse=True):
            w.writerow([n, int(c)])


def save_edge_betweenness_topn(G: nx.DiGraph, top_n: int, out_path: Path) -> None:
    """Edge betweenness centrality hesapla ve ilk N kenarı CSV olarak kaydet."""
    out_path.parent.mkdir(parents=True, exist_ok=True)
    eb = nx.edge_betweenness_centrality(G, normalized=True)
    ranked = sorted(((u, v, s) for (u, v), s in eb.items()), key=lambda t: t[2], reverse=True)[: max(0, top_n)]
    with out_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["u", "v", "edge_betweenness"])
        for u, v, s in ranked:
            w.writerow([u, v, f"{float(s):.6f}"])


# --- Grafik üretim yardımcıları (Matplotlib) ---

def _ensure_matplotlib():
    """Matplotlib'i tembel olarak içe aktar ve varsayılan stili ayarla (TR).

    Bu yardımcı, grafik üreten fonksiyonlar tarafından çağrılır ve
    modül seviyesinde import yerine ihtiyaç olduğunda import eder.
    """
    import importlib

    plt = importlib.import_module("matplotlib.pyplot")
    # Basit, okunaklı bir stil
    try:
        import matplotlib

        matplotlib.rcParams.update({
            "figure.dpi": 120,
            "savefig.dpi": 120,
            "axes.grid": True,
            "grid.linestyle": ":",
        })
    except Exception:
        pass
    return plt


def _save_pair(plt, fig, out_base: Path) -> None:
    """Bir grafiği hem PNG hem SVG olarak kaydet (TR)."""
    out_base.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(str(out_base.with_suffix(".png")))
    fig.savefig(str(out_base.with_suffix(".svg")))
    plt.close(fig)


def plot_degree_histograms(in_deg: Dict[str, int], out_deg: Dict[str, int], out_dir: Path) -> None:
    """In/Out-degree dağılımlarını log-ölçekte histogram olarak kaydet (TR)."""
    plt = _ensure_matplotlib()
    import numpy as np

    xs_in = np.array([v for v in in_deg.values() if v is not None], dtype=float)
    xs_out = np.array([v for v in out_deg.values() if v is not None], dtype=float)

    fig, ax = plt.subplots(1, 2, figsize=(10, 4))
    for i, (title, data) in enumerate((
        ("In-Degree", xs_in),
        ("Out-Degree", xs_out),
    )):
        ax[i].hist(data, bins=50, color="#7c3aed", alpha=0.8)
        ax[i].set_xscale("log")
        ax[i].set_xlabel(title)
        ax[i].set_ylabel("Frekans")
        ax[i].set_title(f"{title} Dağılımı (log ölçek)")
    _save_pair(plt, fig, out_dir / "degree_histograms")


def plot_scatter_correlations(in_deg: Dict[str, int], out_deg: Dict[str, int], btw: Dict[str, float], out_dir: Path) -> None:
    """Korelasyon saçılım grafikleri: (in_degree vs betweenness) ve (in_degree vs out_degree) (TR)."""
    plt = _ensure_matplotlib()
    import numpy as np

    # Sıralı eşleştirme için ortak düğümler
    nodes = sorted(set(in_deg) & set(out_deg) & set(btw))
    xin = np.array([in_deg.get(n, 0) for n in nodes], dtype=float)
    xout = np.array([out_deg.get(n, 0) for n in nodes], dtype=float)
    xbtw = np.array([btw.get(n, 0.0) for n in nodes], dtype=float)

    fig, ax = plt.subplots(1, 2, figsize=(10, 4))
    ax[0].scatter(xin, xbtw, s=6, alpha=0.5, color="#22c55e")
    ax[0].set_xscale("log")
    ax[0].set_xlabel("In-Degree (log)")
    ax[0].set_ylabel("Betweenness")
    ax[0].set_title("In-Degree vs Betweenness")

    ax[1].scatter(xin, xout, s=6, alpha=0.5, color="#60a5fa")
    ax[1].set_xscale("log")
    ax[1].set_yscale("log")
    ax[1].set_xlabel("In-Degree (log)")
    ax[1].set_ylabel("Out-Degree (log)")
    ax[1].set_title("In-Degree vs Out-Degree")

    _save_pair(plt, fig, out_dir / "scatter_correlations")


def plot_topk_bars(
    in_deg: Dict[str, int],
    out_deg: Dict[str, int],
    btw: Dict[str, float],
    risk: Dict[str, float],
    out_dir: Path,
    k: int = 10,
) -> None:
    """In/Out/Betweenness ve birleşik risk için ilk k sütun grafiklerini kaydet (TR)."""
    plt = _ensure_matplotlib()
    import numpy as np

    def _bar_plot(pairs: List[Tuple[str, float]], title: str, out_name: str, color: str) -> None:
        labels = [p[0] for p in pairs]
        vals = np.array([p[1] for p in pairs], dtype=float)
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.barh(range(len(vals)), vals, color=color, alpha=0.85)
        ax.set_yticks(range(len(labels)))
        ax.set_yticklabels(labels, fontsize=8)
        ax.invert_yaxis()
        ax.set_title(title)
        _save_pair(plt, fig, out_dir / out_name)

    top_in = sorted(in_deg.items(), key=lambda kv: kv[1], reverse=True)[:k]
    top_out = sorted(out_deg.items(), key=lambda kv: kv[1], reverse=True)[:k]
    top_btw = sorted(btw.items(), key=lambda kv: kv[1], reverse=True)[:k]
    top_risk = sorted(risk.items(), key=lambda kv: kv[1], reverse=True)[:k]

    _bar_plot(top_in, "İlk 10 In-Degree", "top10_in_degree", "#7c3aed")
    _bar_plot(top_out, "İlk 10 Out-Degree", "top10_out_degree", "#22c55e")
    _bar_plot([(n, float(v)) for n, v in top_btw], "İlk 10 Betweenness", "top10_betweenness", "#60a5fa")
    _bar_plot([(n, float(v)) for n, v in top_risk], "Bileşik Liderler (Risk)", "top10_leaders", "#f59e0b")


def plot_risk_vs_cascade(risk: Dict[str, float], cascade: Dict[str, int], out_dir: Path) -> None:
    """Risk skoru ile kaskad etki büyüklüğü saçılım grafiğini kaydet (TR)."""
    plt = _ensure_matplotlib()
    import numpy as np

    nodes = sorted(set(risk) & set(cascade))
    xs = np.array([risk.get(n, 0.0) for n in nodes], dtype=float)
    ys = np.array([cascade.get(n, 0) for n in nodes], dtype=float)

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.scatter(xs, ys, s=10, alpha=0.5, color="#f59e0b")
    ax.set_xlabel("Risk Skoru")
    ax.set_ylabel("Ters Yönde Etkilenen Paket Sayısı")
    ax.set_title("Risk vs. Basamaklanma Etkisi")
    _save_pair(plt, fig, out_dir / "risk_vs_cascade")


def plot_top_risk(risk: Dict[str, float], out_dir: Path, k: int = 20) -> None:
    """Top k risk skorunu yatay çubuk grafik olarak kaydet (TR)."""
    plt = _ensure_matplotlib()
    import numpy as np

    top = sorted(risk.items(), key=lambda kv: kv[1], reverse=True)[:k]
    labels = [t[0] for t in top]
    vals = np.array([t[1] for t in top], dtype=float)
    fig, ax = plt.subplots(figsize=(10, 7))
    ax.barh(range(len(vals)), vals, color="#f59e0b", alpha=0.85)
    ax.set_yticks(range(len(labels)))
    ax.set_yticklabels(labels, fontsize=8)
    ax.invert_yaxis()
    ax.set_title(f"Top {k} Risk Skoru")
    _save_pair(plt, fig, out_dir / f"top{k}_risk")


def plot_network_visualizations(
    G: nx.DiGraph,
    top_set: Set[str],
    out_dir: Path,
    max_nodes: int = 600,
) -> None:
    """Ağ için iki görselleştirme üret: (1) Top N + tüm bağımlılıklar, (2) yalnızca Top N alt-ağı (TR).

    Büyük grafiklerde çizim maliyetini sınırlamak için en büyük bağlı bileşenden ve/veya
    Top N düğümlerinden örnekleme yapılır. Düğüm boyutu in-degree ile orantılanır.
    """
    plt = _ensure_matplotlib()
    import numpy as np

    W = G.to_undirected()
    comps = list(nx.connected_components(W))
    nodes_full: List[str]
    if comps:
        giant = max(comps, key=len)
        nodes_full = list(giant)
    else:
        nodes_full = list(G.nodes())

    # Çizim örneklemesi (çok büyükse kısıtla)
    if len(nodes_full) > max_nodes:
        nodes_full = nodes_full[:max_nodes]
    H_full = G.subgraph(nodes_full).copy()

    # TopN-only alt ağ
    nodes_top = sorted([n for n in top_set if n in G])
    if len(nodes_top) > max_nodes:
        nodes_top = nodes_top[:max_nodes]
    H_top = G.subgraph(nodes_top).copy()

    def _draw(H: nx.DiGraph, title: str, out_name: str) -> None:
        if H.number_of_nodes() == 0:
            return
        pos = nx.spring_layout(H.to_undirected(), seed=42, k=None)
        indeg = dict(H.in_degree())
        sizes = np.array([max(3.0, indeg.get(n, 0) * 0.8 + 3.0) for n in H.nodes()], dtype=float)
        colors = ["#f59e0b" if n in top_set else "#60a5fa" for n in H.nodes()]
        fig, ax = plt.subplots(figsize=(8, 8))
        ax.set_title(title)
        ax.axis("off")
        nx.draw_networkx_edges(H, pos, ax=ax, width=0.3, alpha=0.25, edge_color="#93c5fd")
        nx.draw_networkx_nodes(H, pos, ax=ax, node_size=sizes, node_color=colors, alpha=0.9)
        _save_pair(plt, fig, out_dir / out_name)

    _draw(H_full, "Top N + Bağımlılıklar", "network_full_topN")
    _draw(H_top, "Sadece Top N Alt-Ağ", "network_topN_only")
