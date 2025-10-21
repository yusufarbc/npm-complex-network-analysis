import json
from pathlib import Path

p = Path('analysis.ipynb')
nb = json.loads(p.read_text(encoding='utf-8'))

# Update imports cell: remove read_list import, add SAMPLE_K and pass cache path
for cell in nb['cells']:
    if cell.get('cell_type')=='code':
        src = cell.get('source', [])
        joined = '\n'.join(src)
        if 'from analysis_helpers import (' in joined:
            cell['source'] = [
              l for l in src if 'read_list' not in l
            ]
        if 'TOP_N =' in joined and 'SAMPLE_K' not in joined:
            # add SAMPLE_K after TOP_N line
            new=[]
            for l in cell['source']:
                new.append(l)
                if l.strip().startswith('TOP_N ='):
                    new.append("SAMPLE_K = None  # Betweenness örnekleme (None=tahmine dayalı)")
            cell['source'] = new
            break

# Update build/metrics call cells
for cell in nb['cells']:
    if cell.get('cell_type')=='code':
        src='\n'.join(cell.get('source', []))
        if 'G, top_set = build_dependency_graph(top_packages)' in src:
            cell['source'] = [ s.replace('build_dependency_graph(top_packages)', "build_dependency_graph(top_packages, cache_path=OUTDIR / 'cache_deps.json')") for s in cell['source'] ]
        if 'in_deg, out_deg, btw = compute_metrics(G)' in src:
            cell['source'] = [ s.replace('compute_metrics(G)', 'compute_metrics(G, sample_k=SAMPLE_K)') for s in cell['source'] ]

p.write_text(json.dumps(nb, ensure_ascii=False, indent=2), encoding='utf-8')
print('OK')
