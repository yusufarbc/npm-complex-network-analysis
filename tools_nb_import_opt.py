import json
from pathlib import Path

p = Path('analysis.ipynb')
nb = json.loads(p.read_text(encoding='utf-8'))

# 1) Ensure unified imports in the first code cell
first_code_idx = next((i for i,c in enumerate(nb['cells']) if c.get('cell_type')=='code'), None)
if first_code_idx is None:
    raise SystemExit('No code cell found')
first = nb['cells'][first_code_idx]
src = first.get('source', [])
joined = '\n'.join(src)
needed_imports = [
    'import json',
    'import numpy as np',
]
# Insert needed imports after existing import block
new_src = []
inserted = False
for line in src:
    new_src.append(line)
    # after OUTDIR import block start adding if not present
    if not inserted and line.strip().startswith('import networkx as nx'):
        # ensure analysis_helpers import follows, then add numpy/json
        pass
for imp in needed_imports:
    if imp not in joined:
        # place before params (TOP_N) if possible
        try:
            idx = next(i for i,l in enumerate(new_src) if l.strip().startswith('TOP_N ='))
            new_src.insert(idx, imp + '\n')
        except StopIteration:
            new_src.append(imp + '\n')
first['source'] = new_src

# 2) Strip duplicate imports in subsequent code cells
DUP_PREFIXES = (
    'import matplotlib',
    'import matplotlib.pyplot as plt',
    'import numpy as np',
    'import json',
)
for i,c in enumerate(nb['cells']):
    if i == first_code_idx: 
        continue
    if c.get('cell_type')=='code':
        cleaned = []
        for line in c.get('source', []):
            if any(line.strip().startswith(pfx) for pfx in DUP_PREFIXES):
                # skip duplicate import
                continue
            cleaned.append(line)
        c['source'] = cleaned

p.write_text(json.dumps(nb, ensure_ascii=False, indent=2), encoding='utf-8')
print('OK')
