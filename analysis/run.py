"""
Komut satırı ile uçtan uca analiz çalıştırıcısı.

Adımlar:
- Top N paket listesini çek (tercihen ecosyste.ms; yedekler: npm search / npms.io)
- En güncel sürüm bağımlılıklarını sorgula ve yönlü bağımlılık ağı kur (Dependent -> Dependency)
- in-degree, out-degree, betweenness merkeziyetlerini hesapla (büyük graph için örnekleme)
- Min–max normalize + ağırlıklarla bileşik risk skoru üret
- (İsteğe bağlı) kantil tabanlı risk sınıflandırması yap ve çıktı ver
- Kenar/metrikler/risk/istatistik/cascade/edge-betweenness çıktıları results/ altına yaz

Kullanım:
  python -m analysis.run --topN 200 --sample-k 200 --classify
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np

from . import __name__ as _pkg_name  # noqa: F401 (paketin import edilebilirliğini doğrular)
from .analysis_helpers import (
    fetch_top_packages,
    build_dependency_graph,
    compute_metrics,
    compute_risk_scores,
    save_edges,
    save_metrics,
    save_risk_scores,
    save_graph_stats,
    cascade_impact_counts,
    save_cascade_impact,
    save_edge_betweenness_topn,
)


def _quantile_bins(values: Dict[str, float], q: List[float]) -> Dict[str, str]:
    """Değerleri verilen kantil eşiklerine göre etiketle.

    Örn: q=[0.7, 0.9] ise etiketler: Low (<=q1), Medium (q1..q2], High (>q2)
    """
    if not values:
        return {}
    xs = np.array(list(values.values()), dtype=float)
    # Eşikleri güvenli hesapla (NaN kaçın)
    xs = xs[~np.isnan(xs)]
    if xs.size == 0:
        return {k: "Low" for k in values}
    qs = np.quantile(xs, q)
    q1 = float(qs[0]) if len(qs) >= 1 else float("nan")
    q2 = float(qs[1]) if len(qs) >= 2 else float("nan")

    labels: Dict[str, str] = {}
    for k, v in values.items():
        vv = float(v)
        if np.isnan(vv) or (not np.isfinite(vv)):
            labels[k] = "Low"
            continue
        if not np.isnan(q2) and vv > q2:
            labels[k] = "High"
        elif not np.isnan(q1) and vv > q1:
            labels[k] = "Medium"
        else:
            labels[k] = "Low"
    return labels


def _write_top_packages(names: List[str], out_dir: Path) -> None:
    p = out_dir / "top_packages.txt"
    out_dir.mkdir(parents=True, exist_ok=True)
    p.write_text("\n".join(names), encoding="utf-8")


def _save_classification(
    labels: Dict[str, str],
    risk: Dict[str, float],
    in_deg: Dict[str, int],
    out_deg: Dict[str, int],
    btw: Dict[str, float],
    out_path: Path,
) -> None:
    import csv

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["package", "tier", "risk_score", "in_degree", "out_degree", "betweenness"])
        for n in sorted(labels.keys()):
            w.writerow([
                n,
                labels.get(n, "Low"),
                f"{float(risk.get(n, 0.0)):.6f}",
                int(in_deg.get(n, 0)),
                int(out_deg.get(n, 0)),
                f"{float(btw.get(n, 0.0)):.6f}",
            ])


def run(
    top_n: int,
    sample_k: int | None,
    include_peer_deps: bool,
    out_dir: Path,
    do_classify: bool,
    quantiles: Tuple[float, float],
    risk_weights: Tuple[float, float, float],
    edge_btw_topn: int,
    cascade_topn: int,
) -> None:
    # 1) Top N paket isimleri
    names = fetch_top_packages(limit=top_n)
    _write_top_packages(names, out_dir)

    # 2) Bağımlılık grafiği (Dependent -> Dependency)
    G, top_set = build_dependency_graph(names, cache_path=out_dir / "cache_deps.json", include_peer_deps=include_peer_deps)

    # 3) Metrikler
    in_deg, out_deg, btw = compute_metrics(G, sample_k=sample_k)

    # 4) Bileşik risk
    w_in, w_out, w_btw = risk_weights
    risk = compute_risk_scores(in_deg, out_deg, btw, w_in=w_in, w_out=w_out, w_btw=w_btw)

    # 5) Çıktılar
    save_edges(G, out_dir / "edges.csv")
    save_metrics(in_deg, out_deg, btw, top_set, out_dir / "metrics.csv")
    save_risk_scores(risk, in_deg, out_deg, btw, top_set, out_dir / "risk_scores.csv")
    save_graph_stats(G, out_dir / "graph_stats.json")

    # 6) Kenar betweenness sıralaması (ilk N)
    if edge_btw_topn > 0:
        save_edge_betweenness_topn(G, edge_btw_topn, out_dir / "edge_betweenness_top10.csv")

    # 7) Kaskad etki (ters yön dependents) — en riskli ilk N düğüm için
    if cascade_topn > 0 and risk:
        seeds = [n for n, _ in sorted(risk.items(), key=lambda kv: kv[1], reverse=True)[:cascade_topn]]
        impact = cascade_impact_counts(G, seeds)
        save_cascade_impact(impact, out_dir / "cascade_impact_top20.csv")

    # 8) Kantile dayalı sınıflandırma
    if do_classify:
        q = list(quantiles)
        labels = _quantile_bins(risk, q)
        _save_classification(labels, risk, in_deg, out_deg, btw, out_dir / "classification.csv")


def main() -> None:
    ap = argparse.ArgumentParser(description="NPM bağımlılık ağı analizi (CLI)")
    ap.add_argument("--topN", type=int, default=200, help="Top N paket sayısı (varsayılan: 200)")
    ap.add_argument("--sample-k", type=int, default=200, help="Betweenness örnekleme k (varsayılan: 200; küçük grafiklerde tam hesap)")
    ap.add_argument("--include-peer-deps", action="store_true", help="peerDependencies alanını da ekle")
    ap.add_argument("--out-dir", type=str, default="results", help="Çıktı klasörü (varsayılan: results)")
    ap.add_argument("--classify", action="store_true", help="Risk skorlarına göre sınıflandırma CSV üret")
    ap.add_argument(
        "--quantiles",
        type=str,
        default="0.7,0.9",
        help="Sınıflandırma kantilleri (örn. '0.7,0.9' → Low/Medium/High)",
    )
    ap.add_argument(
        "--risk-weights",
        type=str,
        default="0.5,0.2,0.3",
        help="Risk ağırlıkları: w_in,w_out,w_btw (varsayılan: 0.5,0.2,0.3)",
    )
    ap.add_argument("--edge-btw-topn", type=int, default=10, help="İlk N edge betweenness çıktı (varsayılan: 10; 0 → kapalı)")
    ap.add_argument("--cascade-topn", type=int, default=20, help="Kaskad etki için tohum sayısı (varsayılan: 20; 0 → kapalı)")

    args = ap.parse_args()

    # Parametreleri ayrıştır
    try:
        qparts = [float(x.strip()) for x in args.quantiles.split(",") if x.strip()]
        if len(qparts) == 1:
            qparts = [qparts[0], min(0.99, max(qparts[0] + 0.2, qparts[0]))]
        quantiles = (min(max(qparts[0], 0.0), 1.0), min(max(qparts[1], 0.0), 1.0))
    except Exception:
        quantiles = (0.7, 0.9)

    try:
        wparts = [float(x.strip()) for x in args.risk_weights.split(",") if x.strip()]
        if len(wparts) != 3:
            wparts = [0.5, 0.2, 0.3]
        s = sum(wparts)
        if s <= 0:
            wparts = [0.5, 0.2, 0.3]
        else:
            wparts = [w / s for w in wparts]
        risk_weights = (wparts[0], wparts[1], wparts[2])
    except Exception:
        risk_weights = (0.5, 0.2, 0.3)

    out_dir = Path(args.out_dir)

    run(
        top_n=int(args.topN),
        sample_k=int(args.sample_k) if args.sample_k and int(args.sample_k) > 0 else None,
        include_peer_deps=bool(args.include_peer_deps),
        out_dir=out_dir,
        do_classify=bool(args.classify),
        quantiles=quantiles,
        risk_weights=risk_weights,
        edge_btw_topn=int(args.edge_btw_topn),
        cascade_topn=int(args.cascade_topn),
    )


if __name__ == "__main__":
    main()

