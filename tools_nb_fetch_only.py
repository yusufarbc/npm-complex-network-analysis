import json
from pathlib import Path
p = Path('analysis.ipynb')
nb = json.loads(p.read_text(encoding='utf-8'))

# Update intro markdown bullet about data source
intro = nb['cells'][0]
if intro.get('cell_type')=='markdown':
    src = intro['source']
    intro['source'] = [
        s.replace("- Veri: `data/top_200.txt` (varsa otomatik kullanılır)", "- Veri: API'den çekilen Top N paket (varsayılan 200)")
         for s in src
    ]

# Update imports/params cell: remove INPUT_LIST / USE_INPUT_LIST lines
for cell in nb['cells']:
    if cell.get('cell_type')=='code':
        lines = cell.get('source', [])
        joined = "\n".join(lines)
        if "INPUT_LIST = Path('data/top_200.txt')" in joined:
            new = []
            for line in lines:
                if line.strip().startswith("INPUT_LIST ") or line.strip().startswith("USE_INPUT_LIST "):
                    continue
                new.append(line)
            cell['source'] = new
            break

# Replace Top 200 load cell to always fetch
for i, cell in enumerate(nb['cells']):
    if cell.get('cell_type')=='markdown' and any('Top 200 Paketleri Yükle' in s for s in cell.get('source', [])):
        # next code cell
        code = nb['cells'][i+1]
        code['source'] = [
            "top_packages = fetch_top_packages(TOP_N)",
            "print(f'API’lerden {len(top_packages)} paket çekildi')",
            "len(top_packages), top_packages[:20]",
        ]
        break

p.write_text(json.dumps(nb, ensure_ascii=False, indent=2), encoding='utf-8')
print('OK')
