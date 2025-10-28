## NPM Complex Network Analysis

NPM ekosistemindeki paketleri yönlü bir ağ olarak modelleyip merkeziyet metrikleriyle yapısal riski ölçer. Amaç, klasik zafiyet skorlarının ötesine geçerek paketin ağ içindeki konumundan doğan sistemik riski görünür kılmaktır.

Canlı önizleme: https://yusufarbc.github.io/npm-complex-network-analysis/

### Proje Yapısı (Özet)
- `analysis/` – Notebook ve yardımcı Python kodları; veriyi çeker, grafı kurar, metrikleri hesaplar.
- `results/` – Üretilen CSV/JSON, görseller ve LaTeX tabloları.
- `academic/` – LaTeX rapor kaynakları ve PDF’ler.
- `.github/` – GitHub Pages dağıtım iş akışı.
- `index.html` – Sonuçların statik sunumu (GitHub Pages).

### Hızlı Başlangıç
Önkoşul: Python 3.10+

1) Sanal ortamı kur ve etkinleştir
   Windows PowerShell:
   ```
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```
2) Bağımlılıkları yükle
   ```
   pip install -r analysis/requirements.txt
   ```
3) Notebook’u aç ve çalıştır
   ```
   python -m pip install notebook  # yoksa
   python -m notebook  # analysis/analysis.ipynb’i açın
   ```
4) Çıktıları incele
   - Üretilen dosyalar `results/` altına yazılır (CSV/PNG/SVG/JSON, .tex tablolar).
   - LaTeX tablolarını tekrar üretmek için: `python results/make_tables.py`
5) Sunumu görüntüle
   - Yerel: `index.html`
   - GitHub Pages: repo ayarlarına göre otomatik dağıtım

### Kısa Notlar
- Kenarlar Dependent → Dependency yönündedir; ters yayılım (dependents) için grafın tersi kullanılır.
- API çağrıları (ecosyste.ms, npm registry) sırasında disk önbelleği kullanılır (`results/cache_deps.json`).
- Büyük graflarda betweenness hesabı örnekleme ile hızlandırılabilir (bkz. `analysis/analysis_helpers.py`).

### Ortam ve Sürümler
- Python: 3.10+ (3.11.9 ile test edildi)
- Numpy: Python 3.11 için `numpy>=1.23` gereklidir (requirements dosyasında tanımlıdır).
- Notebook kullanımı opsiyoneldir (`notebook`, `ipykernel`).

### Alternatif: CLI ile çalıştır
- Notebook olmadan veri ve tabloları üretmek için:
  ```
  python -m analysis.run --topN 200 --sample-k 200
  ```
  - Çıktılar `results/` altına yazılır; LaTeX tabloları otomatik üretilir.
