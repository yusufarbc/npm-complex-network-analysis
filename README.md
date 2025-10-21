# NPM Complex Network Analysis

Bu proje, NPM ekosistemindeki paketleri yönlü bir ağ olarak modelleyip yapısal riski merkeziyet metrikleriyle analiz eder. Hedef, klasik güvenlik metriklerinin (ör. CVSS) ötesine geçerek, bir paketin bağımlılık ağındaki konumundan kaynaklanan sistemik riski görünür kılmaktır.

## Öz

- Ağ: Yönlü grafik (NetworkX `DiGraph`)
- Düğüm: NPM paketi
- Kenar: Bağımlılık ilişkisi
- Yön: Dependent → Dependency (bağımlı paket → bağımlılık)
- Metrikler: In-Degree (pakete gelen kenar), Betweenness (en kısa yollardaki aracı rol)

## Kaynak ve Kapsam

- Varsayılan örneklem: `data/top_200.txt` içindeki Top 200 paket (downloads’a göre). Bu liste npm‑leaderboard ile aynı veri hattına dayalıdır.
- Bağımlılıklar: NPM registry’deki en güncel sürümün `dependencies` alanı temel alınır.
- Not: Varsayılan analiz yalnızca `dependencies` kullanır; `peerDependencies` vb. isteğe bağlı olarak eklenebilir.

## Kurulum

Önkoşullar: Python 3.10+

```
python -m venv .venv
./.venv/Scripts/activate  # Windows PowerShell
pip install -r requirements.txt
```

## Kullanım

Top 200 sabit listesinden ağ ve metrikler:

```
python src/analyze_npm_network.py --input-list data/top_200.txt --outdir results
```

Not defterinden (Jupyter) etkileşimli çalışma:

1) `analysis.ipynb` dosyasını açın.
2) Hücreleri sırayla çalıştırın. Varsayılan olarak `data/top_200.txt` varsa onu kullanır; yoksa API’lerden Top‑N çeker.

İsteğe bağlı – Top 20.000 ismi yalnızca liste olarak indir (graf kurmadan):

```
python src/analyze_npm_network.py --top 20000 --outdir results --list-only
```

## Üretilen Dosyalar (`--outdir` altında, varsayılan `results/`)

- `edges.csv`: Kenar listesi (source=dependent, target=dependency)
- `metrics.csv`: `package,in_degree,betweenness,is_top100`
- `report.md`: In-degree ve betweenness için kısa sıralamalar (tüm düğümler ve Top‑N kohortu)
- `top_packages.txt`: Kullanılan Top‑N isimleri (girdi listesinin kopyası)

## Model Varsayımları ve Sınırlamalar

- Kenar yönü Dependent → Dependency olarak modellenmiştir; bu, ele geçirilme senaryolarında etkilenebilecek paketleri takip etmeyi kolaylaştırır.
- `dependencies` dışındaki alanlar (örn. `peerDependencies`) varsayılan analizde dışarıda tutulur; dahil etmek için betiğe bayrak eklenebilir.
- Dependent (bağımlı) sayıları, yalnızca kohort içindeki bağlantılar üzerinden in-degree ile gözlemlenir. Tüm ekosistemdeki global bağımlı sayısı için ecosyste.ms API’sinden `dependent_packages_count` metriği ayrıca çekilebilir.
- En son sürüm baz alınır; ekosistemde yaygın kullanılan eski sürümlerin bağımlılık yapısı farklı olabilir.

## Yol Haritası / Öneriler

- `peerDependencies` desteğini opsiyonel bayrakla ekleme
- Büyük kohortlar (2k–20k) için yaklaşık betweenness (k-sampling) ve hız sınırlama/yeniden deneme stratejileri
- GEXF/GraphML dışa aktarma ile Gephi/veya diğer araçlara görselleştirme

## Proje Yapısı

- `src/analyze_npm_network.py`: Top‑N’i alır veya dosyadan okur, NetworkX ile grafı kurar, metrikleri hesaplar ve çıktıları üretir.
- `analysis.ipynb`: Adım adım defter; Top‑N getirme, ağ kurma, metrik hesaplama ve saklama.
- `data/top_200.txt`: Kanonik Top 200 listesi (sürüm kontrollü). Diğer `data/*` çıktıları git tarafından yok sayılır.
