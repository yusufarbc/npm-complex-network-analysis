import json
from pathlib import Path

p = Path('analysis.ipynb')
nb = json.loads(p.read_text(encoding='utf-8'))

# 1) Promote step 5 to combined heading and explanation
for i, cell in enumerate(nb['cells']):
    if cell.get('cell_type')=='markdown':
        src = '\n'.join(cell.get('source', []))
        if '## 5) Liderler: İlk 10 (Metin)' in src or '## 5) Liderler: İlk 10 (Metin)' in src:
            cell['source'] = [
                '## 5) Liderler: İlk 10 (Özet + Görselleştirme)',
                'Bu adımda in-degree / out-degree / betweenness için ilk 10’u hem metin olarak özetler hem de bar grafikleri PNG+SVG olarak results/ klasörüne kaydeder.'
            ]
            break

# 2) Remove the separate visualization step header (## 6) ...)
rm_index = None
for i, cell in enumerate(nb['cells']):
    if cell.get('cell_type')=='markdown':
        src = '\n'.join(cell.get('source', []))
        if '## 6) Liderler: İlk 10 (Görselleştirme)' in src:
            rm_index = i
            break
if rm_index is not None:
    nb['cells'].pop(rm_index)

# 3) Decrement subsequent step numbers by 1 (7..15 -> 6..14)
replace_map = {
    '## 7) Sonuçları Kaydet': '## 6) Sonuçları Kaydet',
    '## 8) Hızlı Doğrulama': '## 7) Hızlı Doğrulama',
    '## 9) Tüm Ağ Çizimi (Top N + Bağımlılıklar)': '## 8) Tüm Ağ Çizimi (Top N + Bağımlılıklar)',
    '## 10) Sadece Top N (İndüklenmiş Alt-Ağ)': '## 9) Sadece Top N (İndüklenmiş Alt-Ağ)',
    '## 11) Derece Dağılımları (Histogram)': '## 10) Derece Dağılımları (Histogram)',
    '## 12) Korelasyonlar (Dağılım Grafikleri)': '## 11) Korelasyonlar (Dağılım Grafikleri)',
    '## 13) Bağlanırlık ve Bileşenler': '## 12) Bağlanırlık ve Bileşenler',
    '## 14) Köprü Kenarlar (Edge Betweenness)': '## 13) Köprü Kenarlar (Edge Betweenness)',
    '## 15) Varsayımlar ve Sınırlamalar': '## 14) Varsayımlar ve Sınırlamalar',
}
for cell in nb['cells']:
    if cell.get('cell_type')=='markdown':
        txt = '\n'.join(cell.get('source', []))
        for a,b in replace_map.items():
            if a in txt:
                txt = txt.replace(a,b)
        cell['source'] = txt.split('\n')

p.write_text(json.dumps(nb, ensure_ascii=False, indent=2), encoding='utf-8')
print('OK')
