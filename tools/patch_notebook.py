import json, re
from pathlib import Path

p = Path('analysis.ipynb')
nb = json.loads(p.read_text(encoding='utf-8'))

cells = nb.get('cells', [])

def md(text):
    return {"cell_type":"markdown", "metadata":{}, "source":[text]}

anchors = [
    (r"save_risk_scores\(", "> Çıktı Notu: Risk skorları kaydedildi (risk_scores.csv); Top 20 görseller üretildi."),
    (r"robustness_risk\.json", "> Çıktı Notu: Robustluk sonuçları kaydedildi (robustness_risk.json)."),
    (r"degree_histograms\.png\'\)\;|degree_histograms\.png\'\)\s*", "> Çıktı Notu: In/Out-degree histogramları kaydedildi (degree_histograms.*)."),
    (r"scatter_correlations\.png|scatter_correlations\.svg", "> Çıktı Notu: Korelasyon saçılımları kaydedildi (scatter_correlations.*)."),
]

j = 0
while j < len(cells):
    c = cells[j]
    if c.get('cell_type')=='code':
        src = ''.join(c.get('source',[]))
        for pat, note in anchors:
            if re.search(pat, src):
                cells.insert(j+1, md(note))
                j += 1
                break
    j += 1

nb['cells'] = cells
p.write_text(json.dumps(nb, ensure_ascii=False, indent=1), encoding='utf-8')
print('Notebook patched with additional output notes.')
