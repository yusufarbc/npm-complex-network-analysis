# NPM Complex Network Analysis

Bu proje, NPM ekosistemindeki paketleri yönlü bir ağ olarak modelleyip yapısal riski merkeziyet metrikleriyle analiz eder. Hedef, klasik güvenlik metriklerinin (ör. CVSS) ötesine geçerek, bir paketin bağımlılık ağındaki konumundan kaynaklanan sistemik riski görünür kılmaktır.

## Öz
- Ağ: Yönlü grafik (NetworkX `DiGraph`)
- Düğüm: NPM paketi
- Kenar: Bağımlılık ilişkisi (Dependent → Dependency)
- Metrikler: In-Degree, Out-Degree, Betweenness

## Kapsam ve Veri
- Örneklem: Popüler Top N paket (varsayılan 200)
- Veri: Liste her çalıştırmada API’lerden çekilir (npm registry / ecosyste.ms / npms.io yedekli)
- Bağımlılıklar: NPM registry’deki en güncel sürümün `dependencies` alanı

## Kurulum
Önkoşullar: Python 3.10+
```
python -m venv .venv
./.venv/Scripts/activate  # Windows PowerShell
pip install -r requirements.txt
```

## Kullanım (Notebook)
- `analysis.ipynb` dosyasını açın ve hücreleri sırayla çalıştırın.
- Liste her çalıştırmada API’lerden çekilir; tüm çıktılar `results/` dizinine kaydedilir.

## Üretilen Dosyalar (results/)
- `edges.csv`: Kenar listesi (source=dependent, target=dependency)
- `metrics.csv`: `package,in_degree,out_degree,betweenness,is_top100`
- `report.md`: Kısa sıralamalar (in/out/between; tüm düğümler ve Top N)
- `top_packages.txt`: Kullanılan Top N isimleri (kopya)
- Görseller:
  - `network_full_topN.png/.svg` — Tüm ağ
  - `network_topN_only.png/.svg` — Sadece Top 200 alt-ağ
  - `top10_in_degree.png`, `top10_out_degree.png`, `top10_betweenness.png`, `top10_leaders.png`

## Varsayımlar ve Sınırlamalar
- Kenar yönü Dependent → Dependency; yayılım analizi için uygundur.
- Varsayılan analiz yalnızca `dependencies` alanını içerir; `peerDependencies` isteğe bağlı eklenebilir.
- Global dependent sayıları dahil değildir; ecosyste.ms’ten eklenebilir.
- En güncel sürüm kullanılır; eski sürümlerde bağımlılıklar farklı olabilir.

## Proje Yapısı
- `analysis_helpers.py`: Yardımcı fonksiyonların tamamı (Türkçe açıklamalı)
- `analysis.ipynb`: Adım adım analiz, görseller ve çıktı üretimi

