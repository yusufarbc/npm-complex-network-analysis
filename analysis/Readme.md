## analysis/ — Not defterleri ve yardımcı kodlar

Amaç
- Popüler NPM paketlerinden yönlü bir bağımlılık ağı kurmak.
- in-degree, out-degree ve betweenness merkeziyetlerini hesaplamak.
- Metrikleri min–max ile normalize edip bileşik bir “yapısal risk” skoru üretmek.
- (Opsiyonel) kantil tabanlı risk sınıflandırmasıyla paketleri Low/Medium/High katmanlarına ayırmak.

İçerik
- `analysis.ipynb` — Adım adım veri çekme, ağ kurma, metrikler ve görselleştirme.
- `analysis_helpers.py` — API istemcileri, önbellek, metrik ve çıktı yardımcıları.
- `run.py` — CLI ile uçtan uca analiz (graf → metrik → risk → sınıflandırma → çıktılar).
- `requirements.txt` — Çalışma zamanı bağımlılıkları.

Yöntem ve Metrikler
- Ağ modeli: Düğümler paketleri, kenarlar Dependent → Dependency yönünü temsil eder. Self-loop yoktur; grafik yönlüdür (DiGraph).
- in-degree: Bir pakete kaç paket bağımlı (merkez çekim/çekirdek etkisi). Kaynak: `dict(G.in_degree())`.
- out-degree: Paket kaç bağımlılığa bağlı (kırılgan yüzeyin genişliği). Kaynak: `dict(G.out_degree())`.
- betweenness centrality: Akışın aralarından geçtiği köprü düğümler. Büyük graflarda örnekleme ile hızlandırılır (`--sample-k`).

Normalizasyon
- Tüm metrikler min–max ile [0,1] aralığına dönüştürülür: x' = (x − min) / (max − min).
- Tüm değerler eşitse 0 atanır (bölme-sıfır hatası engellenir).

Bileşik Risk Skoru
- Formül: risk = w_in·in' + w_out·out' + w_btw·btw'
- Varsayılan ağırlıklar: 0.5, 0.2, 0.3 (sırasıyla in, out, btw). CLI ile değiştirilebilir: `--risk-weights w_in,w_out,w_btw`.
- Amaç: Paket içi zafiyetlerden bağımsız olarak ağ topolojisinden doğan yapısal riski görünür kılmak.

Ağ Kurma (Veri Toplama)
- Yön: Dependent → Dependency. Kenarlar bu yöndedir.
- En güncel sürümden `dependencies` alanı okunur; istenirse `peerDependencies` de dahil edilir (`--include-peer-deps`).
- HTTP oturumu yeniden kullanılır, 3 denemeye kadar tekrar yapılır; disk önbelleği: `results/cache_deps.json`.

Sınıflandırma (Opsiyonel)
- Kantil tabanlı üç seviye: Low (≤ q1), Medium (q1..q2], High (> q2)
- Varsayılan eşikler: 0.7 ve 0.9 (CLI: `--quantiles 0.7,0.9`).
- Çıktı: `results/classification.csv`.

Ek Analizler
- Kenar betweenness: En yüksek köprü kenarlar (`results/edge_betweenness_top10.csv`).
- Kaskad etki (ters yön dependents): Tohum düğümlerin etkileyebileceği düğüm sayısı (`results/cascade_impact_top20.csv`).
- Genel istatistikler: Düğüm/kenar sayısı, bileşenler, LCC çapı (mümkünse) → `results/graph_stats.json`.

İşlem Hattı (CLI `analysis/run.py`)
1) Top N paket adları → `results/top_packages.txt`
2) Bağımlılık grafiği → `results/edges.csv`
3) Metrikler (in/out/btw) → `results/metrics.csv`
4) Bileşik risk → `results/risk_scores.csv`
5) (Opsiyonel) sınıflandırma → `results/classification.csv`
6) Kenar betweenness (ilk N) → `results/edge_betweenness_top10.csv`
7) Kaskad etki (ilk N riskli paket) → `results/cascade_impact_top20.csv`
8) Grafik özet istatistikleri → `results/graph_stats.json`

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
   python -m notebook  # analysis/analysis.ipynb dosyasını açın
   ```
3) Çıktılar `results/` altına yazılır (CSV/PNG/SVG/JSON, .tex tablolar).

Kullanım (CLI)
Hızlı çalışma:
```
python -m analysis.run --topN 200 --sample-k 200 --classify
```
Seçili bayraklar:
- `--include-peer-deps` → `peerDependencies` dahil et.
- `--risk-weights 0.5,0.2,0.3` → risk ağırlıkları (in,out,btw).
- `--quantiles 0.7,0.9` → sınıflandırma eşikleri.
- `--edge-btw-topn 10`, `--cascade-topn 20` → ek analiz kapsamı.

Bağımlılıklar ve Ortam
- Python 3.11+ (önerilen 3.11.9)
- `networkx`, `requests`, `matplotlib`, `scipy`, `numpy` (bkz. `analysis/requirements.txt`)

İpuçları
- Büyük graflarda betweenness için örnekleme (`--sample-k`) kullanın.
- API yanıtlarındaki geçici sorunlar için önbellek yardımcı olur: `results/cache_deps.json`.
- Örneklemeli betweenness için rastgelelik tohumlanır (seed=42) → tekrarlanabilirlik.

Sınırlılıklar
- Betweenness hesaplaması büyük graflarda pahalı olabilir; örnekleme şiddetle tavsiye edilir.
- NPM API limitleri geçici veri eksikliğine yol açabilir; tekrar denemeleri ve önbellek ile azaltılır.

