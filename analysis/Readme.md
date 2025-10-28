## analysis/ – Not defterleri ve yardımcı kodlar

Amaç: Popüler NPM paketlerinden yönlü bağımlılık ağı kurmak, merkeziyet metrikleri (in/out-degree, betweenness) ve bileşik risk skorlarını üretmek.

İçerik
- `analysis.ipynb` – Adım adım veri çekme, ağ kurma, metrikler ve görselleştirme.
- `analysis_helpers.py` – API istemcileri, önbellek, metrik ve çıktı yardımcıları.
- `requirements.txt` – Çalışma zamanı bağımlılıkları.

Kullanım (Notebook)
1) Ortamı hazırlayın
   ```
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1  # Windows PowerShell
   pip install -r analysis/requirements.txt
   python -m pip install notebook
   ```
2) Not defterini açın ve hücreleri sırayla çalıştırın
   ```
   python -m notebook  # analysis/analysis.ipynb’i açın
   ```
3) Çıktılar `results/` altına yazılır (CSV/PNG/SVG/JSON, .tex tablolar)

Bağımlılıklar
- Python 3.10+
- `networkx`, `requests`, `matplotlib`, `scipy` (bkz. `requirements.txt`)

Notlar/İpuçları
- API çağrılarında disk önbelleği kullanılır: `results/cache_deps.json`.
- Büyük graflarda betweenness için örnekleme (k) kullanmak işlemi hızlandırır.
- Opsiyonel `peerDependencies` dahil edilebilir (yardımcı fonksiyondaki `include_peer_deps`).

CLI (Notebook’suz)
```
python -m analysis.run --topN 200 --sample-k 200
```
Çıktılar `results/` altına yazılır; mümkünse LaTeX tabloları otomatik üretilir.

Ortam ve Sürümler
- Python: 3.11.x kullanın (önerilen 3.11.9)
- Python 3.11 için NumPy alt sınırı: `numpy>=1.23` (requirements’ta yer alır)
