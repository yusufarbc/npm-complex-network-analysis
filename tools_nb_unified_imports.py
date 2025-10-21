import json
from pathlib import Path

p = Path('analysis.ipynb')
nb = json.loads(p.read_text(encoding='utf-8'))

# Find first code cell
first_code_idx = next((i for i,c in enumerate(nb['cells']) if c.get('cell_type')=='code'), None)
if first_code_idx is None:
    raise SystemExit('No code cell found')

# Build unified import + params cell
first_code = {
  'cell_type': 'code',
  'execution_count': None,
  'metadata': {},
  'outputs': [],
  'source': [
    "# İçe aktarımlar ve temel parametreler\n",
    "from pathlib import Path\n",
    "import sys\n",
    "import os\n",
    "\n",
    "# Matplotlib kontrol/kurulum (gerekirse)\n",
    "try:\n",
    "    import matplotlib  # noqa: F401\n",
    "    import matplotlib.pyplot as plt  # noqa: F401\n",
    "    print('matplotlib hazır')\n",
    "except ModuleNotFoundError:\n",
    "    import subprocess\n",
    "    print('matplotlib eksik; kuruluyor...')\n",
    "    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'matplotlib'])\n",
    "    import matplotlib  # noqa: F401\n",
    "    import matplotlib.pyplot as plt  # noqa: F401\n",
    "    print('kurulum tamam')\n",
    "\n",
    "import networkx as nx\n",
    "from analysis_helpers import (\n",
    "    fetch_top_packages,\n",
    "    build_dependency_graph,\n",
    "    compute_metrics,\n",
    "    save_edges,\n",
    "    save_metrics,\n",
    "    save_report,\n",
    "    read_list,\n",
    ")\n",
    "\n",
    "TOP_N = 1000  # Top N paket (varsayılan)\n",
    "OUTDIR = Path('results')\n",
    "OUTDIR.mkdir(parents=True, exist_ok=True)\n",
    "OUTDIR\n",
  ]
}

# Replace first code cell with unified version
nb['cells'][first_code_idx] = first_code

# Remove any separate matplotlib ensure cell (search by marker text)
rm_indices = []
for i, c in enumerate(nb['cells']):
    if c.get('cell_type')=='code':
        src = '\n'.join(c.get('source', []))
        if 'Matplotlib kontrol/kurulum' in src and i != first_code_idx:
            rm_indices.append(i)

for i in sorted(rm_indices, reverse=True):
    nb['cells'].pop(i)

p.write_text(json.dumps(nb, ensure_ascii=False, indent=2), encoding='utf-8')
print('OK')
