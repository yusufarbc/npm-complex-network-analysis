import json
from pathlib import Path

p = Path('analysis.ipynb')
nb = json.loads(p.read_text(encoding='utf-8'))

# Replace intro cell with richer Turkish content
intro_md = [
  "# NPM Kompleks Ağ Analizi (Top N)",
  "",
  "Bu defter, popüler Top N NPM paketini yönlü bir ağ (Dependent → Dependency) olarak modelleyip, in-degree / out-degree / betweenness merkeziyet metrikleriyle yapısal riski inceler.",
  "",
  "Amaç:",
  "- Bağımlılık ağındaki konuma dayalı kritik düğümleri belirlemek",
  "- Zincirleme etki potansiyelini (cascading impact) nicel olarak görmek",
  "- Sonuçları tekrar üretilebilir şekilde görselleştirmek ve raporlamak",
  "",
  "Metodoloji (özet):",
  "- Veri: Liste her çalıştırmada API’lerden çekilir (ecosyste.ms / npm registry / npms.io yedekli)",
  "- Ağ: NetworkX DiGraph (kenar: Dependent → Dependency)",
  "- Metrikler: In-Degree (gelen), Out-Degree (giden), Betweenness",
  "- Performans: Büyük graf’larda betweenness için örneklemeli hesap",
  "- Çıktılar: Tüm sonuçlar `results/` klasörüne yazılır (CSV/MD/JSON + PNG/SVG)",
  "",
  "Varsayılan Top N = 1000 (değiştirilebilir)."
]
nb['cells'][0]['source'] = intro_md

# Fix section that mentions analysis_helpers location
for cell in nb['cells']:
    if cell.get('cell_type')=='markdown':
        s = '\n'.join(cell.get('source', []))
        if 'src/analyze_npm_network.py' in s:
            cell['source'] = [s.replace('src/analyze_npm_network.py', 'analysis_helpers.py')]

# Clean code cell: remove sys.path append for src; rename comment
for cell in nb['cells']:
    if cell.get('cell_type')=='code':
        src_lines = cell.get('source', [])
        changed = False
        new_lines = []
        for line in src_lines:
            if "sys.path.append(str(Path('src').resolve()))" in line:
                changed = True
                continue
            if line.strip().startswith('# Tercihen sabit Top 200 listesi'):
                new_lines.append('# Parametreler\n')
                changed = True
                continue
            new_lines.append(line)
        if changed:
            cell['source'] = new_lines

# Update Top N load markdown
for cell in nb['cells']:
    if cell.get('cell_type')=='markdown':
        src = '\n'.join(cell.get('source', []))
        if 'Top N Paketleri Yükle' in src:
            cell['source'] = [
                '## 2) Top N Paketleri Yükle',
                '',
                'Liste her çalıştırmada API’lerden çekilir (indirme sayısına göre sıralı).'
            ]
            break

# Update any remaining titles containing "Top 200"
for cell in nb['cells']:
    if cell.get('cell_type')=='code':
        cell['source'] = [
            l.replace("NPM Top 200 Bağımlılık Ağı", "NPM Top N Bağımlılık Ağı")
             for l in cell.get('source', [])
        ]

# Save
p.write_text(json.dumps(nb, ensure_ascii=False, indent=2), encoding='utf-8')
print('OK')
