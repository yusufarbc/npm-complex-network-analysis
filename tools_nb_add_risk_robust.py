import json
from pathlib import Path

p = Path('analysis.ipynb')
nb = json.loads(p.read_text(encoding='utf-8'))

# 1) Update first code cell: add INCLUDE_PEER_DEPS and RISK_WEIGHTS
for cell in nb['cells']:
    if cell.get('cell_type')=='code':
        src = cell.get('source', [])
        joined='\n'.join(src)
        if 'TOP_N =' in joined and 'INCLUDE_PEER_DEPS' not in joined:
            new=[]
            for l in src:
                new.append(l)
                if l.strip().startswith('TOP_N ='):
                    new.append("INCLUDE_PEER_DEPS = False  # peerDependencies'i eklemek icin True yapin")
                    new.append("RISK_WEIGHTS = (0.5, 0.2, 0.3)  # (w_in, w_out, w_btw)")
            cell['source']=new
            break

# 2) Update graph build call to pass include_peer_deps
for cell in nb['cells']:
    if cell.get('cell_type')=='code':
        cell['source'] = [ s.replace("build_dependency_graph(top_packages, cache_path=OUTDIR / 'cache_deps.json')",
                                     "build_dependency_graph(top_packages, cache_path=OUTDIR / 'cache_deps.json', include_peer_deps=INCLUDE_PEER_DEPS)")
                           for s in cell.get('source', []) ]

# 3) Append Risk Score section
nb['cells'].append({
  'cell_type':'markdown','metadata':{},
  'source':["## 13) Risk Skoru (Bileşik)", "Normalize in/out/between ile ağırlıklı (w_in,w_out,w_btw) risk skoru. İlk 20’yi dışa aktaralım ve görselleştirelim."]
})
nb['cells'].append({
  'cell_type':'code','metadata':{},'execution_count':None,'outputs':[],
  'source':[
    'from analysis_helpers import compute_risk_scores, save_risk_scores',
    'risk = compute_risk_scores(in_deg, out_deg, btw, *RISK_WEIGHTS)',
    "save_risk_scores(risk, in_deg, out_deg, btw, top_set, OUTDIR / 'risk_scores.csv')",
    '# İlk 20 risk liderini görselleştir (PNG+SVG)',
    'top20 = sorted(risk.items(), key=lambda kv: kv[1], reverse=True)[:20]',
    "names = [n for n,_ in top20][::-1]; vals=[v for _,v in top20][::-1]",
    'import matplotlib.pyplot as plt',
    "plt.figure(figsize=(8,8), dpi=150); plt.barh(names, vals, color='tab:red'); plt.title('Risk Skoru İlk 20'); plt.xlabel('Risk'); plt.tight_layout();",
    "plt.savefig(OUTDIR / 'top20_risk.png'); plt.savefig(OUTDIR / 'top20_risk.svg')",
    '(len(risk), len(top20))'
  ]
})

# 4) Append Robustness section (by risk removals)
nb['cells'].append({
  'cell_type':'markdown','metadata':{},
  'source':["## 14) Robustluk Analizi (Risk Tabanlı Kaldırma)", "Risk skoruna göre ilk 1/3/5 düğümü kaldırınca bağlanırlık nasıl değişiyor?"]
})
nb['cells'].append({
  'cell_type':'code','metadata':{},'execution_count':None,'outputs':[],
  'source':[
    'import json',
    'from analysis_helpers import robustness_remove_and_stats',
    'ranked = [n for n,_ in sorted(risk.items(), key=lambda kv: kv[1], reverse=True)]',
    'ks = [1,3,5]',
    'results = {}',
    'for k in ks:',
    '    removed = ranked[:k]',
    '    stats = robustness_remove_and_stats(G, removed)',
    '    results[str(k)] = {"removed": removed, "stats": stats}',
    "(OUTDIR / 'robustness_risk.json').write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding='utf-8')",
    'results'
  ]
})

p.write_text(json.dumps(nb, ensure_ascii=False, indent=2), encoding='utf-8')
print('OK')
