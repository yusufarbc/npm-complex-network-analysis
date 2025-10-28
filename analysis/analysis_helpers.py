"""
Yardimci fonksiyonlar (TR):
- Top N paket listesini cek (ecosyste.ms oncelikli; npm search / npms.io yedek).
- En guncel surumden dependencies cek.
- Yonu Dependent -> Dependency olan yonlu ag kur.
- Merkeziyet metriklerini (in/out-degree, betweenness) hesapla.
- Sonuclari CSV/MD olarak kaydet. Basit disk onbellegi ve retry icerir.

Not: Bu modul analysis.ipynb tarafindan kullanilir.
"""

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


# ecosyste.ms uzerinden tek sayfada (<=1000) Top N paket adlarini cek
def _fetch_top_packages_ecosystems(limit: int) -> List[str]:
    """ecosyste.ms paket adlarini tek sayfa (<=1000) olarak, indirmeye gore siralayarak cek."""
    per_page = min(max(limit, 1), 1000)
    params = {"per_page": per_page, "sort": "downloads", "page": 1}
    resp = requests.get(ECOSYSTEMS_PACKAGE_NAMES_URL, params=params, timeout=60)
    resp.raise_for_status()
    names: List[str] = resp.json()
    return names[:limit]


# ecosyste.ms uzerinden sayfalayarak (per_page=1000) Top N paket adlarini topla
def _fetch_top_packages_ecosystems_paginated(limit: int) -> List[str]:
    """ecosyste.ms uzerinden sayfalayarak limit adede kadar paket adi topla (per_page=1000)."""
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
    # Sira korunarak tekillestir
    seen: Set[str] = set()
    deduped: List[str] = []
    for name in collected:
        if name and name not in seen:
            seen.add(name)
            deduped.append(name)
        if len(deduped) >= limit:
            break
    return deduped


# npms.io populerlik skoruna gore yaklasik Top N paket adlarini cek (yedek)
def _fetch_top_packages_npms(limit: int) -> List[str]:
    """npms.io populerlik skorunu yaklasik olarak kullanarak isim listesi cek."""
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


# Top N paket adlarini getir (oncelik ecosyste.ms; npm search / npms.io yedek)
def fetch_top_packages(limit: int = 100) -> List[str]:
    """En cok indirilen Top N paket adlarini getir (tercihen ecosyste.ms, ardindan yedekler)."""
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
    # npm registry aramasi (popularity) yedegi
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


# NPM paket adini URL icin guvenli bicimde kodla (scoped paketler dahil)
def encode_npm_name(name: str) -> str:
    """NPM paket adini URL yolunda guvenli kullanmak icin kodla (scoped paketlerde '/' da kodlanir)."""
    return quote(name, safe="")


# Bir paketin en guncel surumunden dependencies alanini cek
def fetch_dependencies(
    package: str,
    session: Optional[requests.Session] = None,
    include_peer: bool = False,
) -> Dict[str, str]:
    """Paketin npm registry'deki en guncel surumunden `dependencies` alanini cek.

    Daha verimli olmak icin paylasilan bir `requests.Session` (varsa) kullanir.
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


# Basit disk onbellegi (JSON) — bagimlilik sorgulari icin
def _load_cache(path: Path) -> Dict[str, Dict[str, str]]:
    """Onbellegi yukle (yoksa bos sozluk)."""
    try:
        if path.exists():
            import json
            return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        pass
    return {}


def _save_cache(path: Path, cache: Dict[str, Dict[str, str]]) -> None:
    """Onbellegi diske yaz (guvenli yazim)."""
    try:
        import json, tempfile
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp = Path(tempfile.gettempdir()) / (path.name + ".tmp")
        tmp.write_text(json.dumps(cache, ensure_ascii=False), encoding="utf-8")
        tmp.replace(path)
    except Exception:
        pass


# Top N listesinden yonlu bagimlilik agi kur (Dependent -> Dependency)
def build_dependency_graph(
    top_packages: List[str],
    cache_path: Optional[Path] = None,
    include_peer_deps: bool = False,
) -> Tuple[nx.DiGraph, Set[str]]:
    """Top N listesi icin yonlu bir bagimlilik agi (Dependent -> Dependency) kur ve dondur.

    Baglanti maliyetini azaltmak icin tek bir HTTP oturumu (Session) yeniden kullanilir.
    """
    G = nx.DiGraph()
    top_set: Set[str] = set(top_packages)
    for pkg in top_packages:
        G.add_node(pkg)
    cache: Dict[str, Dict[str, str]] = {}
    if cache_path is None:
        cache_path = Path("results/cache_deps.json")
    cache = _load_cache(cache_path)
    with requests.Session() as session:
        for pkg in top_packages:
            # Onbellegin kullanilmasi
            deps: Dict[str, str]
            if pkg in cache:
                deps = cache.get(pkg) or {}
            else:
                # Basit 3 denemeli cekim
                deps = {}
                for _ in range(3):
                    deps = fetch_dependencies(pkg, session=session, include_peer=include_peer_deps)
                    if deps:
                        break
                cache[pkg] = deps
            for dep in deps.keys():
                # NetworkX add_edge implicitly adds missing nodes
                G.add_edge(pkg, dep)  # Dependent -> Dependency
    _save_cache(cache_path, cache)
    return G, top_set


# Ag icin in-degree, out-degree ve betweenness metriklerini hesapla
def compute_metrics(
    G: nx.DiGraph, sample_k: Optional[int] = None
) -> Tuple[Dict[str, int], Dict[str, int], Dict[str, float]]:
    """Ag icin in-degree, out-degree ve betweenness merkeziyet metriklerini hesapla.

    Buyuk graflarda (ornegin >1200 dugum) betweenness icin ornekleme (k)
    kullanarak hesabi hizlandirir. sample_k verilirse o deger esas alinir.
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


# --- Risk skoru (bilesik) ---
def _minmax_norm(values: Dict[str, float]) -> Dict[str, float]:
    """Min‑max normalize et (tum degerler ayniysa 0 dondur)."""
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
    """Normalize (min‑max) edilmis in/out/between ile bilesik risk skoru hesapla."""
    # float donusturme
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
    """Risk skorlarini CSV olarak kaydet (paket, risk, in, out, between, is_topN)."""
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
    """Belirtilen dugumler kaldirildiktan sonra baglanirlik istatistikleri (zayif)."""
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
    # En buyuk bilesen icin cap (diameter) hesaplamayi dene
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


# Dugum metriklerini CSV olarak kaydet (in_degree, out_degree, betweenness)
def save_metrics(
    in_deg: Dict[str, int],
    out_deg: Dict[str, int],
    btw: Dict[str, float],
    top_set: Set[str],
    out_path: Path,
) -> None:
    """Dugum metriklerini CSV olarak kaydet (paket, in_degree, out_degree, betweenness, is_topN)."""
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


# Kisa bir Markdown raporu uret (in/out/between icin ilk 20 listeler)
def save_report(
    in_deg: Dict[str, int], out_deg: Dict[str, int], btw: Dict[str, float], top_set: Set[str], out_path: Path
) -> None:
    """Kisa bir Markdown raporu uret ve kaydet (in/out/between icin ilk 20 listeler)."""
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
    lines.append("# NPM Bagimlilik Agi Raporu")
    lines.append("")
    lines.append("## In-Degree Ilk 20 (Tum Dugumler)")
    for n, v in top_in_all:
        lines.append(f"- {n}: {v}")
    lines.append("")
    lines.append("## Out-Degree Ilk 20 (Tum Dugumler)")
    for n, v in top_out_all:
        lines.append(f"- {n}: {v}")
    lines.append("")
    lines.append("## Betweenness Ilk 20 (Tum Dugumler)")
    for n, v in top_btw_all:
        lines.append(f"- {n}: {v:.6f}")
    lines.append("")
    lines.append("## In-Degree Ilk 20 (Top N Kohortu)")
    for n, v in top_in_top:
        lines.append(f"- {n}: {v}")
    lines.append("")
    lines.append("## Out-Degree Ilk 20 (Top N Kohortu)")
    for n, v in top_out_top:
        lines.append(f"- {n}: {v}")
    lines.append("")
    lines.append("## Betweenness Ilk 20 (Top N Kohortu)")
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
    """Cascade etki sayaçlarını CSV olarak kaydet (seed, impacted_count)."""
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
