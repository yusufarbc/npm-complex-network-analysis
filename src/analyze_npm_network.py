import argparse
import csv
import os
from pathlib import Path
from typing import Dict, List, Set, Tuple

import networkx as nx
import requests
from requests.utils import quote


ECOSYSTEMS_PACKAGE_NAMES_URL = (
    "https://packages.ecosyste.ms/api/v1/registries/npmjs.org/package_names"
)
NPMS_SEARCH_URL = "https://api.npms.io/v2/search"
NPM_SEARCH_URL = "https://registry.npmjs.org/-/v1/search"
NPM_REGISTRY_BASE = "https://registry.npmjs.org"


def _fetch_top_packages_ecosystems(limit: int) -> List[str]:
    """Single page fetch (kept for small N)."""
    per_page = min(max(limit, 1), 1000)
    params = {"per_page": per_page, "sort": "downloads", "page": 1}
    resp = requests.get(ECOSYSTEMS_PACKAGE_NAMES_URL, params=params, timeout=60)
    resp.raise_for_status()
    names: List[str] = resp.json()
    return names[:limit]


def _fetch_top_packages_ecosystems_paginated(limit: int) -> List[str]:
    """Paginate ecosystems API to collect up to `limit` names.

    The endpoint supports `per_page<=1000` and `page` starting from 1.
    We sort by downloads to approximate a "most downloaded" Top-N.
    """
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
            # last page reached
            break
    # Deduplicate while preserving order
    seen: Set[str] = set()
    deduped: List[str] = []
    for name in collected:
        if name and name not in seen:
            seen.add(name)
            deduped.append(name)
        if len(deduped) >= limit:
            break
    return deduped


def _fetch_top_packages_npms(limit: int) -> List[str]:
    # Use npms.io popularity as a fallback approximation
    params = {"q": "scope:public", "size": min(limit, 250)}
    resp = requests.get(NPMS_SEARCH_URL, params=params, timeout=60)
    resp.raise_for_status()
    data = resp.json()
    results = data.get("results", [])
    # Sort locally by popularity score if present
    results.sort(
        key=lambda r: (r.get("score", {}).get("detail", {}).get("popularity", 0.0)),
        reverse=True,
    )
    names = [r.get("package", {}).get("name") for r in results if r.get("package")]
    return [n for n in names if n][:limit]


def fetch_top_packages(limit: int = 100) -> List[str]:
    # Prefer ecosystems paginated for large N (e.g., 20k), single-page for small.
    try:
        if limit > 1000:
            names = _fetch_top_packages_ecosystems_paginated(limit)
            if names:
                return names
        # Small N fast path
        names = _fetch_top_packages_ecosystems(limit)
        if names:
            return names
    except Exception:
        pass
    # Try npm registry search sorted by popularity as fallback
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
    # Fallback to npms.io search popularity
    names = _fetch_top_packages_npms(limit)
    return names


def encode_npm_name(name: str) -> str:
    # Encode fully for path usage; scoped packages require encoding '/'
    return quote(name, safe="")


def fetch_dependencies(package: str) -> Dict[str, str]:
    encoded = encode_npm_name(package)
    url = f"{NPM_REGISTRY_BASE}/{encoded}"
    resp = requests.get(url, timeout=60)
    if resp.status_code != 200:
        return {}
    data = resp.json()

    # Prefer latest tag; fallback to dist-tags if available; else try max version
    latest = None
    try:
        latest = data.get("dist-tags", {}).get("latest")
    except Exception:
        latest = None

    versions = data.get("versions", {}) if isinstance(data, dict) else {}
    version_obj = None
    if latest and latest in versions:
        version_obj = versions.get(latest, {})
    elif versions:
        # Fallback: pick the lexicographically last version as a crude proxy
        # (semver-aware sort would need extra deps; acceptable for quick analysis)
        try:
            version_key = sorted(versions.keys())[-1]
            version_obj = versions.get(version_key, {})
        except Exception:
            version_obj = {}
    else:
        version_obj = {}

    deps = version_obj.get("dependencies", {}) if isinstance(version_obj, dict) else {}
    if not isinstance(deps, dict):
        return {}
    return deps


def build_dependency_graph(top_packages: List[str]) -> Tuple[nx.DiGraph, Set[str]]:
    G = nx.DiGraph()
    top_set = set(top_packages)
    for pkg in top_packages:
        G.add_node(pkg)
    for pkg in top_packages:
        deps = fetch_dependencies(pkg)
        for dep in deps.keys():
            # Edge direction: Dependent -> Dependency
            G.add_edge(pkg, dep)
            if dep not in G:
                G.add_node(dep)
    return G, top_set


def compute_metrics(G: nx.DiGraph) -> Tuple[Dict[str, int], Dict[str, float]]:
    in_deg: Dict[str, int] = dict(G.in_degree())
    # Betweenness on directed graphs; normalization keeps values in [0,1]
    # For larger graphs this can be expensive; here the graph is modest.
    btw: Dict[str, float] = nx.betweenness_centrality(G, normalized=True)
    return in_deg, btw


def save_edges(G: nx.DiGraph, out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["source", "target"])  # Dependent -> Dependency
        for u, v in G.edges():
            w.writerow([u, v])


def save_metrics(
    in_deg: Dict[str, int],
    btw: Dict[str, float],
    top_set: Set[str],
    out_path: Path,
) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["package", "in_degree", "betweenness", "is_top100"])
        all_nodes = set(in_deg.keys()) | set(btw.keys())
        for n in sorted(all_nodes):
            w.writerow([n, in_deg.get(n, 0), f"{btw.get(n, 0.0):.6f}", str(n in top_set)])


def save_report(
    in_deg: Dict[str, int], btw: Dict[str, float], top_set: Set[str], out_path: Path
) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    # Top by in-degree among all nodes
    top_in_all = sorted(in_deg.items(), key=lambda kv: kv[1], reverse=True)[:20]
    # Top by betweenness among all nodes
    top_btw_all = sorted(btw.items(), key=lambda kv: kv[1], reverse=True)[:20]
    # Focused on the Top-N cohort only
    top_in_top = sorted(
        ((n, in_deg.get(n, 0)) for n in top_set), key=lambda kv: kv[1], reverse=True
    )[:20]
    top_btw_top = sorted(
        ((n, btw.get(n, 0.0)) for n in top_set), key=lambda kv: kv[1], reverse=True
    )[:20]

    lines: List[str] = []
    lines.append("# NPM Dependency Network Report")
    lines.append("")
    lines.append("## Top 20 by In-Degree (All Nodes)")
    for n, v in top_in_all:
        lines.append(f"- {n}: {v}")
    lines.append("")
    lines.append("## Top 20 by Betweenness (All Nodes)")
    for n, v in top_btw_all:
        lines.append(f"- {n}: {v:.6f}")
    lines.append("")
    lines.append("## Top 20 by In-Degree (Top Cohort)")
    for n, v in top_in_top:
        lines.append(f"- {n}: {v}")
    lines.append("")
    lines.append("## Top 20 by Betweenness (Top Cohort)")
    for n, v in top_btw_top:
        lines.append(f"- {n}: {v:.6f}")

    out_path.write_text("\n".join(lines), encoding="utf-8")


def read_list(path: Path) -> list[str]:
    if not path.exists():
        return []
    return [
        line.strip()
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Build a directed dependency graph for Top-N npm packages and compute centralities."
        )
    )
    parser.add_argument("--top", type=int, default=100, help="Number of top packages")
    parser.add_argument(
        "--outdir", type=str, default="data", help="Output directory for artifacts"
    )
    parser.add_argument(
        "--input-list",
        type=str,
        default=None,
        help="Path to a newline-separated package list (overrides fetching)",
    )
    parser.add_argument(
        "--list-only",
        action="store_true",
        help="Only fetch and save the Top-N list, skip dependency graph",
    )
    args = parser.parse_args()

    out_dir = Path(args.outdir)
    out_dir.mkdir(parents=True, exist_ok=True)

    if args.input_list:
        src_list = Path(args.input_list)
        print(f"Reading package list from {src_list} ...")
        top_packages = read_list(src_list)
        print(f"Loaded {len(top_packages)} package names.")
    else:
        print(f"Fetching Top {args.top} packages by downloads...")
        top_packages = fetch_top_packages(args.top)
        print(f"Fetched {len(top_packages)} packages.")

    # Save the cohort list first
    (out_dir / "top_packages.txt").write_text("\n".join(top_packages), encoding="utf-8")
    if args.list_only:
        print("List-only mode: saved Top-N package names; skipping graph build.")
        print(f"- {out_dir / 'top_packages.txt'}")
        return

    print("Building dependency graph (Dependent -> Dependency)...")
    G, top_set = build_dependency_graph(top_packages)
    print(f"Graph nodes: {G.number_of_nodes()}, edges: {G.number_of_edges()}")

    print("Computing centrality metrics (in-degree, betweenness)...")
    in_deg, btw = compute_metrics(G)

    print("Saving artifacts...")
    save_edges(G, out_dir / "edges.csv")
    save_metrics(in_deg, btw, top_set, out_dir / "metrics.csv")
    save_report(in_deg, btw, top_set, out_dir / "report.md")

    print("Done. Artifacts written to:")
    print(f"- {out_dir / 'edges.csv'}")
    print(f"- {out_dir / 'metrics.csv'}")
    print(f"- {out_dir / 'report.md'}")
    print(f"- {out_dir / 'top_packages.txt'}")


if __name__ == "__main__":
    main()
