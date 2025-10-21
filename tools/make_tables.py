import csv
from pathlib import Path


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
        f.write('\\begin{table}[h]\n\\centering\n')
        f.write('\\\\\\caption{Top 20 In-Degree (Toplam Düğümler)}\n')
        f.write('\\begin{tabular}{lrrrr}\n\\toprule\n')
        f.write('Paket & In-Degree & Out-Degree & Betweenness & TopN? \\\\ \\midrule\n')
        for r in top:
            pkg = (r.get('package','') or '').replace('&','\\&')
            indeg = r.get('in_degree', 0)
            outdeg = r.get('out_degree','0')
            btw = r.get('betweenness','0.000000')
            istop = r.get('is_topN', r.get('is_top100','False'))
            f.write(f"{pkg} & {indeg} & {outdeg} & {btw} & {istop} \\\\\n")
        f.write('\\bottomrule\n\\end{tabular}\n\\end{table}\n')
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
        f.write('\\begin{table}[h]\n\\centering\n')
        f.write('\\caption{Top 20 Risk Skoru}\n')
        f.write('\\begin{tabular}{lrrrrr}\n\\toprule\n')
        f.write('Paket & Risk & In-Degree & Out-Degree & Betweenness & TopN? \\\\ \\midrule\n')
        for r in top:
            pkg = (r.get('package','') or '').replace('&','\\&')
            risk = f"{float(r.get('risk_score',0)):.6f}"
            indeg = r.get('in_degree','0')
            outdeg = r.get('out_degree','0')
            btw = r.get('betweenness','0.000000')
            istop = r.get('is_topN','False')
            f.write(f"{pkg} & {risk} & {indeg} & {outdeg} & {btw} & {istop} \\\\\n")
        f.write('\\bottomrule\n\\end{tabular}\n\\end{table}\n')
    return True


def main():
    res = Path('results')
    res.mkdir(exist_ok=True)
    ok1 = write_metrics_top20_in(res)
    ok2 = write_risk_top20(res)
    print('metrics_top20_in_degree.tex', 'OK' if ok1 else 'SKIP')
    print('risk_scores_top20.tex', 'OK' if ok2 else 'SKIP')


if __name__ == '__main__':
    main()






