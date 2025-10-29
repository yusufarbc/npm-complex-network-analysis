# NPM Complex Network Analysis

NPM ekosistemindeki paketleri yönlü bir ağ olarak modeller ve merkeziyet metrikleriyle yapısal riski ölçer. Amaç, klasik zafiyet skorlarının ötesine geçerek, bir paketin ağ içindeki konumundan doğan sistemik riski görünür kılmaktır.

Canlı önizleme: https://yusufarbc.github.io/npm-complex-network-analysis/

## İçindekiler
- Amaç ve Kapsam
- Kullanılan Metrikler ve Yöntemler
- Proje Yapısı
- Hızlı Başlangıç
- Kullanım (Notebook ve CLI)
- Üretilen Çıktılar
- Ortam ve Sürümler
- Güvenlik Bağlamı

## Amaç ve Kapsam
Bu çalışma, popüler NPM paketlerinden yönlü bir bağımlılık ağı kurar; in-degree, out-degree ve betweenness merkeziyetlerini hesaplayıp min–max normalize ederek bileşik bir risk skoru üretir. Böylece, yalnızca paket içi zafiyetlere değil, bağımlılık topolojisinden kaynaklanan yapısal riske de odaklanır.

## Kullanılan Metrikler ve Yöntemler
- Ağ modeli
  - Düğümler paketleri, kenarlar Dependent → Dependency yönünü temsil eder.
  - Self-loop ve çoklu kenar yoktur; grafik yönlüdür (DiGraph).
- Metrikler
  - in-degree: Kaç paket bu pakete bağlı (popüler çekirdeklerin izi).
  - out-degree: Bu paket kaç bağımlılığa bağlı (kırılgan yüzeyin izi).
  - betweenness centrality: Akışın “arasında olma” derecesi (köprü/kilit konumlar).
  - Betweenness büyük graflarda örnekleme ile hızlandırılabilir: `--sample-k`.
- Normalizasyon ve bileşik risk
  - Her metrik min–max normalize edilir: x' = (x - min) / (max - min).
  - Risk formülü (varsayılan ağırlıklar):
    - risk = 0.5·in' + 0.2·out' + 0.3·btw'
    - Ağırlıklar CLI ile değiştirilebilir: `--risk-weights w_in,w_out,w_btw`.
- Sınıflandırma (opsiyonel)
  - Kantil tabanlı ayrım: varsayılan eşikler 0.7 ve 0.9.
  - Etiketler: Low (≤q1), Medium (q1..q2], High (>q2), çıktı: `classification.csv`.
- Ek analizler
  - Edge betweenness: En yüksek köprü kenarlar (`edge_betweenness_top10.csv`).
  - Kaskad etki (ters yön dependents): Seçili tohumlar için etki sayısı (`cascade_impact_top20.csv`).
  - Genel istatistikler: Düğüm/kenar sayısı, bileşenler, LCC çapı (`graph_stats.json`).
- Önbellek ve dayanıklılık
  - HTTP sorguları disk önbelleği ile azaltılır: `results/cache_deps.json`.
  - Bağlantı hatalarında basit tekrarlar uygulanır.

## Proje Yapısı
- `analysis/` — Notebook ve yardımcı Python kodlar (veri çekme, ağ kurma, metrikler, CLI)
- `results/` — Üretilen CSV/JSON, görseller ve LaTeX tablolar
- `academic/` — LaTeX rapor kaynakları ve PDF’ler
- `index.html` — Sonuçların statik sunumu (GitHub Pages)

Detaylar: `analysis/README.md`, `results/README.md`.

## Hızlı Başlangıç
Önkoşul: Python 3.11.x (önerilen 3.11.9)

1) Sanal ortamı kur ve etkinleştir (Windows PowerShell)
```
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```
2) Bağımlılıkları yükle
```
pip install -r analysis/requirements.txt
```
3) Notebook’u aç (opsiyonel)
```
python -m notebook  # analysis/analysis.ipynb dosyasını açın
```
4) Tabloları (LaTeX) üret
```
python analysis/make_tables.py
```
5) Sunumu görüntüle
- Yerel: `index.html`
- GitHub Pages: Actions ile otomatik dağıtım

## Kullanım
### Notebook
- `analysis/analysis.ipynb` dosyasını açın, hücreleri sırayla çalıştırın; tüm çıktılar `results/` içine yazılır.

### CLI
Notebook olmadan üretim:
```
python -m analysis.run --topN 200 --sample-k 200 --classify
```
Seçenekler:
- `--include-peer-deps` → `peerDependencies`’i de dahil et.
- `--risk-weights 0.5,0.2,0.3` → risk ağırlıkları (in,out,btw).
- `--quantiles 0.7,0.9` → sınıflandırma eşikleri.
- `--edge-btw-topn 10` → en yüksek edge betweenness çıktısı.
- `--cascade-topn 20` → kaskad etki için tohum sayısı.

## Üretilen Çıktılar
- `results/edges.csv` — Kenar listesi (source=dependent, target=dependency)
- `results/metrics.csv` — `package,in_degree,out_degree,betweenness,is_topN`
- `results/risk_scores.csv` — Bileşik risk skoru + metrikler
- `results/graph_stats.json` — Genel ağ istatistikleri
- `results/edge_betweenness_top10.csv` — En yüksek köprü kenarlar
- `results/cascade_impact_top20.csv` — Ters yön (dependents) kaskad etkisi
- `results/classification.csv` — (opsiyonel) Low/Medium/High risk sınıfları
- Görseller: `*.png/.svg`; Tablolar: `*.tex` (bkz. `analysis/make_tables.py`)

## Ortam ve Sürümler
- Python: 3.11.x (önerilen 3.11.9)
- NumPy: `>=1.23` (Python 3.11 uyumu için)
- Notebook kullanımı opsiyoneldir (`notebook`, `ipykernel`).

## Güvenlik Bağlamı (özet)
Eylül 2025’te NPM ekosisteminde, popüler paketlerin bakımcı hesaplarının phishing ile ele geçirilmesi sonucu kısa süreli kötü amaçlı sürümler yayımlandı (örnekler: chalk, debug). Olay, bağımlılık ağlarının geniş fan-out’u ve transit bağımlılıkların etkisi nedeniyle ekosistem genelinde yüksek risk potansiyeli taşıdı. Bu proje, benzer olaylarda “yapısal risk”i nicel olarak ortaya koymayı amaçlar.

Seçme kaynaklar:
- Palo Alto Networks: https://www.paloaltonetworks.com/blog/cloud-security/npm-supply-chain-attack/
- CISA: https://www.cisa.gov/news-events/alerts/2025/09/23/widespread-supply-chain-compromise-impacting-npm-ecosystem
- Trend Micro: https://www.trendmicro.com/en_us/research/25/i/npm-supply-chain-attack.html
- Bleeping Computer: https://www.bleepingcomputer.com/news/security/hackers-hijack-npm-packages-with-2-billion-weekly-downloads-in-supply-chain-attack/
- Trellix: https://www.trellix.com/blogs/research/npm-account-hijacking-and-the-rise-of-supply-chain-attacks/

