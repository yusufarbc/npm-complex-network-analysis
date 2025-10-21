# NPM Complex Network Analysis – Usage

This repository fetches Top-N npm packages by downloads, builds a directed dependency network (Dependent -> Dependency), and computes centrality metrics to estimate structural risk.

## Prerequisites

- Python 3.10+

## Setup

```
python -m venv .venv
./.venv/Scripts/activate  # On Windows PowerShell
pip install -r requirements.txt
```

## Run Analysis

```
python src/analyze_npm_network.py --top 100 --outdir data
```

Artifacts:

- `data/edges.csv` — edge list (source=dependent, target=dependency)
- `data/metrics.csv` — node metrics (package, in_degree, betweenness, is_top100)
- `data/report.md` — quick top lists for in-degree and betweenness
- `data/top_packages.txt` — Top-N package names used

Notes:

- Top packages are retrieved from ecosystems API sorted by downloads.
- Dependencies are read from npm registry for each package’s latest version.
- Betweenness centrality is computed on the full graph; reported both overall and for the Top-N cohort.

## Fetch Top 20,000 List Only

If you only need the Top 20,000 by downloads (without building the graph):

```
python src/analyze_npm_network.py --top 20000 --outdir data --list-only
```

This paginates the ecosystems endpoint and writes:

- `data/top_packages.txt`

Tip: Building the full dependency graph for 20k packages can be slow and heavy due to registry rate limits and centrality computation cost. Consider sampling (e.g., 2k–5k) or computing only degree metrics for very large graphs.
