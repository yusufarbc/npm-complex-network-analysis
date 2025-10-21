import json
from pathlib import Path

p = Path('analysis.ipynb')
nb = json.loads(p.read_text(encoding='utf-8'))

# Find first code cell index
first_code_idx = next((i for i,c in enumerate(nb['cells']) if c.get('cell_type')=='code'), None)
if first_code_idx is None:
    first_code_idx = 0

ensure_cell = {
  'cell_type': 'code',
  'execution_count': None,
  'metadata': {},
  'outputs': [],
  'source': [
    "# Matplotlib kontrol/kurulum (gerekirse)",
    "try:",
    "    import matplotlib  # noqa: F401",
    "    print('matplotlib hazır')",
    "except ModuleNotFoundError:",
    "    import sys, subprocess",
    "    print('matplotlib eksik; kuruluyor...')",
    "    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'matplotlib'])",
    "    import matplotlib  # noqa: F401",
    "    print('kurulum tamam')",
  ]
}

# Insert ensure cell right after the first code cell
insert_at = first_code_idx + 1
nb['cells'].insert(insert_at, ensure_cell)

p.write_text(json.dumps(nb, ensure_ascii=False, indent=2), encoding='utf-8')
print('OK')
