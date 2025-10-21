import json
from pathlib import Path

p = Path('analysis.ipynb')
nb = json.loads(p.read_text(encoding='utf-8'))

# Helper to replace text in markdown cell
def replace_in_cell(cell, mapping):
    if cell.get('cell_type')!='markdown':
        return
    src = cell.get('source', [])
    joined = '\n'.join(src)
    for a,b in mapping.items():
        joined = joined.replace(a,b)
    cell['source'] = joined.split('\n')

# 1) Intro title: Top 200 -> Top N and add default note if missing
intro = nb['cells'][0]
replace_in_cell(intro, {
    '# NPM Kompleks Ağ Analizi (Top 200)': '# NPM Kompleks Ağ Analizi (Top N)',
})
if intro.get('cell_type')=='markdown':
    s='\n'.join(intro['source'])
    if 'varsayılan 1000' not in s:
        intro['source'].append('')
        intro['source'].append('Varsayılan Top N = 1000 (değiştirilebilir).')

# 2) Rename section headings to consistent numbering and Top N wording
heading_map = {
    '## 2) Top 200 Paketleri Yükle': '## 2) Top N Paketleri Yükle',
    '## 8) Tüm Ağ Çizimi (Top 200 + Bağımlılıklar)': '## 9) Tüm Ağ Çizimi (Top N + Bağımlılıklar)',
    '## 9) Sadece Top 200 (İndüklenmiş Alt-Ağ)': '## 10) Sadece Top N (İndüklenmiş Alt-Ağ)',
    '## 9) Sadece Top 200 Induklenmis Alt-Ag': '## 10) Sadece Top N Induklenmis Alt-Ag',
    '## 8) Tum Ag Cizimi (Top 200 + Bagimliliklar)': '## 9) Tum Ag Cizimi (Top N + Bagimliliklar)',
}
for cell in nb['cells']:
    replace_in_cell(cell, heading_map)

# 3) Change "İlk 15" section to "Liderler: İlk 10 (Metin)" and slices to 10
for idx, cell in enumerate(nb['cells']):
    if cell.get('cell_type')=='markdown':
        joined='\n'.join(cell.get('source', []))
        if '## 5) İlk 15' in joined or '## 5) Ilk 15' in joined:
            cell['source'] = ['## 5) Liderler: İlk 10 (Metin)', 'In-degree / Out-degree / Betweenness ilk 10 metin özeti.']
            # next code cell slices
            code = nb['cells'][idx+1]
            if code.get('cell_type')=='code':
                new = []
                for line in code.get('source', []):
                    new.append(line.replace('[:15]', '[:10]'))
                code['source'] = new
            break

# 4) Renumber the later leaders visualization section from 11) to 6)
for cell in nb['cells']:
    if cell.get('cell_type')=='markdown':
        replace_in_cell(cell, {'## 11) Liderler: İlk 10 (Görselleştirme)': '## 6) Liderler: İlk 10 (Görselleştirme)'})

# 5) Shift following section numbers by -1 where needed to maintain ordering
number_map = {
    '## 6) Sonuçları Kaydet': '## 7) Sonuçları Kaydet',
    '## 7) Hızlı Doğrulama': '## 8) Hızlı Doğrulama',
    '## 8) Tüm Ağ Çizimi (Top N + Bağımlılıklar)': '## 9) Tüm Ağ Çizimi (Top N + Bağımlılıklar)',
    '## 9) Sadece Top N (İndüklenmiş Alt-Ağ)': '## 10) Sadece Top N (İndüklenmiş Alt-Ağ)',
    '## 12) Derece Dağılımları (Histogram)': '## 11) Derece Dağılımları (Histogram)',
    '## 13) Korelasyonlar (Dağılım Grafikleri)': '## 12) Korelasyonlar (Dağılım Grafikleri)',
    '## 14) Bağlanırlık ve Bileşenler': '## 13) Bağlanırlık ve Bileşenler',
    '## 15) Köprü Kenarlar (Edge Betweenness)': '## 14) Köprü Kenarlar (Edge Betweenness)',
    '## 10) Varsayımlar ve Sınırlamalar': '## 15) Varsayımlar ve Sınırlamalar',
}
for cell in nb['cells']:
    replace_in_cell(cell, number_map)

# 6) Ensure Top N wording in titles without 200 remnants
cleanup_map = {
    'Top 200': 'Top N',
    'Top-200': 'Top N',
}
for cell in nb['cells']:
    replace_in_cell(cell, cleanup_map)

p.write_text(json.dumps(nb, ensure_ascii=False, indent=2), encoding='utf-8')
print('OK')
