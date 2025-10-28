import csv
from pathlib import Path


def _lt_begin(f, caption: str, cols: str, header_line: str) -> None:
    f.write('\\begin{longtable}{' + cols + '}' + '\n')
    f.write('\\caption{' + caption + '}\\\\' + '\n')
    f.write('\\toprule' + '\n')
    f.write(header_line + ' \\\\' + '\n')
    f.write('\\midrule' + '\n')
    f.write('\\endfirsthead' + '\n')
    f.write('\\toprule' + '\n')
    f.write(header_line + ' \\\\' + '\n')
    f.write('\\midrule' + '\n')
    f.write('\\endhead' + '\n')
    f.write('\\bottomrule' + '\n')
    f.write('\\endfoot' + '\n')
    f.write('\\bottomrule' + '\n')
    f.write('\\endlastfoot' + '\n')


def _lt_end(f) -> None:
    f.write('\\end{longtable}' + '\n')


def write_metrics_top20_in(res: Path) -> bool:
    mfile = res / 'metrics.csv'
    if not mfile.exists():
        return False
    with mfile.open(encoding='utf-8') as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        try:
            r['in_degree'] = int(r.get('in_degree', 0))
        except Exception:
            r['in_degree'] = 0
    rows.sort(key=lambda r: r['in_degree'], reverse=True)
    top = rows[:20]
    tex = res / 'metrics_top20_in_degree.tex'
    with tex.open('w', encoding='utf-8') as f:
        _lt_begin(f, 'Top 20 In-Degree (Toplam Dugumler)', 'lrrrr', 'Paket & In-Degree & Out-Degree & Betweenness & TopN?')
        for r in top:
            pkg = (r.get('package','') or '').replace('&','\\&')
            indeg = r.get('in_degree', 0)
            outdeg = r.get('out_degree','0')
            btw = r.get('betweenness','0.000000')
            istop = r.get('is_topN', r.get('is_top100','False'))
            f.write(f"{pkg} & {indeg} & {outdeg} & {btw} & {istop} \\\\" + "\n")
        _lt_end(f)
    return True


def write_risk_top20(res: Path) -> bool:
    rfile = res / 'risk_scores.csv'
    if not rfile.exists():
        return False
    with rfile.open(encoding='utf-8') as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        try:
            r['risk_score'] = float(r.get('risk_score', 0.0))
        except Exception:
            r['risk_score'] = 0.0
    rows.sort(key=lambda r: r['risk_score'], reverse=True)
    top = rows[:20]
    tex = res / 'risk_scores_top20.tex'
    with tex.open('w', encoding='utf-8') as f:
        _lt_begin(f, 'Top 20 Risk Skoru', 'lrrrrr', 'Paket & Risk & In-Degree & Out-Degree & Betweenness & TopN?')
        for r in top:
            pkg = (r.get('package','') or '').replace('&','\\&')
            risk = f"{float(r.get('risk_score',0)):.6f}"
            indeg = r.get('in_degree','0')
            outdeg = r.get('out_degree','0')
            btw = r.get('betweenness','0.000000')
            istop = r.get('is_topN','False')
            f.write(f"{pkg} & {risk} & {indeg} & {outdeg} & {btw} & {istop} \\\\" + "\n")
        _lt_end(f)
    return True


def write_edge_betweenness_top10(res: Path) -> bool:
    p = res / 'edge_betweenness_top10.csv'
    if not p.exists():
        return False
    with p.open(encoding='utf-8') as f:
        rows = list(csv.DictReader(f))
    norm = []
    for r in rows:
        try:
            eb = float(r.get('edge_betweenness', '0') or 0)
        except Exception:
            eb = 0.0
        u = (r.get('u','') or '').replace('&','\\&')
        v = (r.get('v','') or '').replace('&','\\&')
        norm.append((u, v, eb))
    norm.sort(key=lambda t: t[2], reverse=True)
    tex = res / 'edge_betweenness_top10.tex'
    with tex.open('w', encoding='utf-8') as f:
        _lt_begin(f, 'Edge Betweenness Ilk 10 (Yuksek kopru kenarlar)', 'l l r', 'U & V & Edge Betweenness')
        for u,v,eb in norm[:10]:
            f.write(f"{u} & {v} & {eb:.6f} \\\\" + "\n")
        _lt_end(f)
    return True


def write_cascade_impact_top20(res: Path) -> bool:
    p = res / 'cascade_impact_top20.csv'
    if not p.exists():
        return False
    with p.open(encoding='utf-8') as f:
        rows = list(csv.DictReader(f))
    norm = []
    for r in rows:
        name = (r.get('package','') or '').replace('&','\\&')
        try:
            cnt = int(float(r.get('impacted_count', '0') or 0))
        except Exception:
            cnt = 0
        norm.append((name, cnt))
    norm.sort(key=lambda t: t[1], reverse=True)
    tex = res / 'cascade_impact_top20.tex'
    with tex.open('w', encoding='utf-8') as f:
        _lt_begin(f, 'Basamaklanma Etkisi: Top 20 (Ters yonde etkilenebilecek paket sayisi)', 'l r', 'Paket & Etkilenen Paket Sayisi')
        for name, cnt in norm[:20]:
            f.write(f"{name} & {cnt} \\\\" + "\n")
        _lt_end(f)
    return True


def write_metrics_top20_out(res: Path) -> bool:
    mfile = res / 'metrics.csv'
    if not mfile.exists():
        return False
    with mfile.open(encoding='utf-8') as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        try:
            r['out_degree'] = int(r.get('out_degree', 0))
        except Exception:
            r['out_degree'] = 0
    rows.sort(key=lambda r: r['out_degree'], reverse=True)
    top = rows[:20]
    tex = res / 'metrics_top20_out_degree.tex'
    with tex.open('w', encoding='utf-8') as f:
        _lt_begin(f, 'Top 20 Out-Degree (Toplam Dugumler)', 'lrrrr', 'Paket & Out-Degree & In-Degree & Betweenness & TopN?')
        for r in top:
            pkg = (r.get('package','') or '').replace('&','\\&')
            outdeg = r.get('out_degree', 0)
            indeg = r.get('in_degree','0')
            btw = r.get('betweenness','0.000000')
            istop = r.get('is_topN', r.get('is_top100','False'))
            f.write(f"{pkg} & {outdeg} & {indeg} & {btw} & {istop} \\\\" + "\n")
        _lt_end(f)
    return True


def write_metrics_top20_betweenness(res: Path) -> bool:
    mfile = res / 'metrics.csv'
    if not mfile.exists():
        return False
    with mfile.open(encoding='utf-8') as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        try:
            r['betweenness'] = float(r.get('betweenness', 0.0))
        except Exception:
            r['betweenness'] = 0.0
    rows.sort(key=lambda r: r['betweenness'], reverse=True)
    top = rows[:20]
    tex = res / 'metrics_top20_betweenness.tex'
    with tex.open('w', encoding='utf-8') as f:
        _lt_begin(f, 'Top 20 Betweenness (Toplam Dugumler)', 'lrrrr', 'Paket & Betweenness & In-Degree & Out-Degree & TopN?')
        for r in top:
            pkg = (r.get('package','') or '').replace('&','\\&')
            indeg = r.get('in_degree','0')
            outdeg = r.get('out_degree','0')
            btw = f"{float(r.get('betweenness',0.0)):.6f}"
            istop = r.get('is_topN', r.get('is_top100','False'))
            f.write(f"{pkg} & {btw} & {indeg} & {outdeg} & {istop} \\\\" + "\n")
        _lt_end(f)
    return True


def main():
    res = Path('results')
    res.mkdir(exist_ok=True)
    ok1 = write_metrics_top20_in(res)
    ok2 = write_risk_top20(res)
    ok3 = write_edge_betweenness_top10(res)
    ok4 = write_cascade_impact_top20(res)
    ok5 = write_metrics_top20_out(res)
    ok6 = write_metrics_top20_betweenness(res)
    print('metrics_top20_in_degree.tex', 'OK' if ok1 else 'SKIP')
    print('risk_scores_top20.tex', 'OK' if ok2 else 'SKIP')
    print('edge_betweenness_top10.tex', 'OK' if ok3 else 'SKIP')
    print('cascade_impact_top20.tex', 'OK' if ok4 else 'SKIP')
    print('metrics_top20_out_degree.tex', 'OK' if ok5 else 'SKIP')
    print('metrics_top20_betweenness.tex', 'OK' if ok6 else 'SKIP')


if __name__ == '__main__':
    main()
