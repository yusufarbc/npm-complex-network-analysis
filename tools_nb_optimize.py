import json
from pathlib import Path

p = Path('analysis.ipynb')
nb = json.loads(p.read_text(encoding='utf-8'))

# Set TOP_N = 1000
for cell in nb['cells']:
    if cell.get('cell_type')=='code':
        cell['source'] = [ s.replace('TOP_N = 200', 'TOP_N = 1000') for s in cell.get('source', []) ]

# Mention sampling betweenness in metrics markdown
for cell in nb['cells']:
    if cell.get('cell_type')=='markdown':
        s = '\n'.join(cell.get('source', []))
        if '## 4) Merkeziyet Metrikleri' in s and 'örnekleme' not in s and 'ornekleme' not in s:
            cell['source'] = [
                '## 4) Merkeziyet Metrikleri\n',
                '- In-Degree: Düğüme gelen kenar → etkilenebilecek alan\n',
                '- Out-Degree: Düğümün dış bağımlılık sayısı → bağımlılık zinciri uzunluğu\n',
                '- Betweenness: En kısa yollardaki aracılık → tek hata noktası riski\n',
                '\n',
                'Not: Büyük graf’larda betweenness yaklaşık örnekleme (k) ile hızlandırılır.'
            ]
            break

p.write_text(json.dumps(nb, ensure_ascii=False, indent=2), encoding='utf-8')
print('OK')
