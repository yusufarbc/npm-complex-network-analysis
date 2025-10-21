# NPM Complex Network Analysis

Bu proje, NPM ekosistemindeki paketleri yönlü bir ağ olarak modelleyip yapısal riski merkeziyet metrikleriyle analiz eder. Hedef, klasik güvenlik metriklerinin (ör. CVSS) ötesine geçerek, bir paketin bağımlılık ağındaki konumundan kaynaklanan sistemik riski görünür kılmaktır.

## Sunum (index.html)
- Kök dizindeki `index.html`, `results/` altındaki görselleri ve dosyaları açıklamalarıyla birlikte sunar.
- Ayrıntılı açıklamalar `paper/main.tex` ile uyumludur; tam metin için `paper/main.pdf`.
- Not: Depoda `.gitignore` varsayılan olarak `results/` klasörünü dışlar. Uzak depoda sonuçları göstermek istiyorsanız bu klasörü geçici olarak dahil edebilir (`git add -f results/...`) ya da ayrı bir yayın klasörü (örn. `docs/`) kullanabilirsiniz.

- https://yusufarbc.github.io/npm-complex-network-analysis/

## Öz
- Ağ: Yönlü grafik (NetworkX `DiGraph`)
- Düğüm: NPM paketi
- Kenar: Bağımlılık ilişkisi (Dependent → Dependency)
- Metrikler: In-Degree, Out-Degree, Betweenness

## Kapsam ve Veri
- Örneklem: Popüler Top N paket (varsayılan 200)
- Veri: Liste her çalıştırmada API'lerden çekilir (ecosyste.ms öncelikli; npm registry / npms.io yedekli)
- Bağımlılıklar: NPM registry'deki en güncel sürümün `dependencies` alanı (opsiyonel `peerDependencies`)

## Kurulum
Önkoşullar: Python 3.10+
```
python -m venv .venv
./.venv/Scripts/activate  # Windows PowerShell
pip install -r requirements.txt
```

## Kullanım (Notebook)
- `analysis.ipynb` dosyasını açın ve hücreleri sırayla çalıştırın.
- Liste her çalıştırmada API'lerden çekilir; tüm çıktılar `results/` dizinine kaydedilir.

## Üretilen Dosyalar (results/)
- `edges.csv`: Kenar listesi (source=dependent, target=dependency)
- `metrics.csv`: `package,in_degree,out_degree,betweenness,is_topN`
- `risk_scores.csv`: Bileşik risk skorları ve ilgili metrikler
- `report.md`: Kısa sıralamalar (in/out/between; tüm düğümler ve Top N)
- `top_packages.txt`: Kullanılan Top N isimleri (kopya)
- Görseller:
  - `network_full_topN.png/.svg` — Tüm ağ
  - `network_topN_only.png/.svg` — Sadece Top N alt-ağ
  - `degree_histograms.png/.svg`, `scatter_correlations.png/.svg`
  - `top10_in_degree.png`, `top10_out_degree.png`, `top10_betweenness.png`, `top10_leaders.png`
  - `top20_risk.png/.svg`

## Varsayımlar ve Sınırlamalar
- Kenar yönü Dependent → Dependency; yayılım analizi için uygundur.
- Varsayılan analiz yalnızca `dependencies` alanını içerir; `peerDependencies` isteğe bağlı eklenebilir.
- Global dependent sayıları dahil değildir; ecosyste.ms'ten eklenebilir.
- En güncel sürüm kullanılır; eski sürümlerde bağımlılıklar farklı olabilir.

## Proje Yapısı
- `analysis_helpers.py`: Yardımcı fonksiyonlar (Türkçe açıklamalı)
- `analysis.ipynb`: Adım adım analiz, görseller ve çıktı üretimi
- `tools/make_tables.py`: Sonuç CSV’lerinden LaTeX tablo üretimi
- `paper/`: LaTeX makale kaynağı ve PDF

