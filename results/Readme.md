## results/ — Üretilen çıktılar (özet ve yorum)

**Çalışma Tarihi:** Ekim 2025

Bu klasör, analysis/analysis.ipynb çalıştırıldığında üretilen veri dosyaları, görseller ve LaTeX tablolarını içerir. Aşağıdaki bölümler, çıktıları yorumlamayı kolaylaştırmak için topolojik risk bağlamında kısa bir özet, metodoloji ve bulgularla zenginleştirilmiştir.

### Özet (Topolojik Risk Perspektifi)
- NPM bağımlılık ağı ağır kuyruklu (scale‑free) bir yapı sergiler; az sayıda “hub” düğüm, sistemik riskin odağıdır.
- En çok indirilen 1000 paket üzerinden kurulan yönlü ağda, in/out‑degree ve betweenness metrikleri ile Bileşik Risk Skoru (BRS) üretilmiştir.
- BRS (0.5·in' + 0.2·out' + 0.3·btw') hub’ların ve köprü düğümlerin önceliklendirilmesini sağlar; sonuçlar kaskad etki ile uyumludur.
- Robustness analizi, kritik düğümlerin çıkarılmasının ağın bağlanırlığını dramatik biçimde bozabildiğini gösterir.

### Kavramsal Arka Plan (kısa)
- “Miras alınan risk”: Ortalama bir paketin kodunun büyük bölümü transitif bağımlılıklardadır; görünmeyen risk üst katmanlara taşınır.
- Olay örnekleri (left‑pad, event‑stream, 2024‑25 saldırıları) hub kaybının zincirleme etki doğurduğunu göstermiştir.
- SSC (software supply chain) savunması çok katmanlı olmalıdır: tespit (ML/davranışsal), kriptografik doğrulama (SBOM, in‑toto) ve süreç hijyeni.

### Metodoloji: Bileşik Risk Skoru (BRS)
- Ağ: Düğümler paket, kenarlar Dependent → Dependency.
- Metrikler: in‑degree (yayılım potansiyeli), out‑degree (maruziyet yüzeyi), betweenness (köprü/boğaz noktası).
- Normalizasyon: min–max; tüm değerler aynıysa 0 atanır.
- BRS formülü: risk = 0.5·in' + 0.2·out' + 0.3·btw'.
- Kantil sınıfları (ops.): 0.7/0.9 → Low/Medium/High.

### Bulgular ve Yorum
- Derece dağılımı ağır kuyruklu; hub’ların ele geçirilmesi veya kaybı sistemik kırılganlığı artırır.
- in‑degree ile betweenness arasında pozitif ilişki gözlenir; omurga paketler aynı zamanda kritik köprü rolündedir.
- BRS Top 20, tekil metriklerden daha iyi ayrım gücü sağlar; kaskad etki sonuçlarıyla genellikle tutarlıdır (ilişki doğrusal değildir).
- Robustness: En yüksek BRS düğümlerin hedefli çıkarımı, bileşenleşmeyi hızlandırır ve LCC’yi küçültür.
- Örnek gözlemler (tipik): `tslib`, `es-abstract`, `@babel/helper-plugin-utils` gibi altyapı paketleri liderdir ve geniş etki alanı taşır.

### Örnek: Bu Çalıştırmadan BRS Top 5

| Paket | BRS | In-Degree | Out-Degree | Betweenness |
|---|---:|---:|---:|---:|
| prop-types | 0.796663 | 115 | 3 | 0.000071 |
| @swc/helpers | 0.500000 | 118 | 0 | 0.000000 |
| @react-types/shared | 0.427966 | 101 | 0 | 0.000000 |
| @react-aria/utils | 0.399815 | 49 | 6 | 0.000041 |
| @babel/runtime | 0.351695 | 83 | 0 | 0.000000 |

### Stratejik Öneriler (kısa)
- Geliştiriciler: SCA araçlarını CI/CD’ye entegre edin; lock file’ları kullanın ve düzenli güncelleyin; OSSF Scorecards gibi sağlık metriklerine bakın.
- Bakımcılar: İmzalı sürümler, iki kişi kuralı, açık sürüm notları; 2FA ve erişim hijyeni.
- Ekosistem: Paket imzalamayı teşvik/zorunlu kılma; typo‑squatting’e karşı ad benzerlik kontrolleri.

### Veri dosyaları (CSV/JSON)
- `edges.csv` — Bağımlılık kenarları (source=dependent, target=dependency)
  - Yorum: Kenar yönü “bağımlı → bağımlılık” şeklindedir. Bir pakete gelen kenar sayısı (in-degree), o pakete bağımlı paket sayısını gösterir.
- `metrics.csv` — Düğümsel metrikler
  - Sütunlar: `package,in_degree,out_degree,betweenness,is_topN`
  - Yorum: in_degree, yayılım potansiyeli (hub etkisi) için; out_degree, bağımlılık yüzeyi için; betweenness, köprü/boğaz noktası rolü için kullanılır.
- `risk_scores.csv` — Bileşik Risk Skoru (BRS) ve metrikler
  - Sütunlar: `package,risk_score,in_degree,out_degree,betweenness,is_topN`
  - Yorum: BRS = 0.5·in' + 0.2·out' + 0.3·btw' (min–max normalize edilmiş değerler kullanılır). Yüksek BRS, ele geçirilmesi halinde daha geniş/derin etki potansiyeline işaret eder.
- `classification.csv` — (opsiyonel) Kantil tabanlı sınıflar
  - Sütunlar: `package,tier,risk_score,in_degree,out_degree,betweenness`
  - Yorum: Varsayılan kantiller 0.7/0.9; etiketler Low/Medium/High.
- `edge_betweenness_top10.csv` — En yüksek köprü kenarlar (edge betweenness)
- `cascade_impact_top20.csv` — Kaskad etki sayıları (ters yön, dependents)
- `graph_stats.json` — Ağ özet istatistikleri (düğüm/kenar sayısı, bileşenler, LCC çapı vb.)

### Görseller (PNG + SVG)
- `network_full_topN.*` — Top N + bağımlılıklar ağ çizimi (Top N turuncu, diğerleri mavi; düğüm boyutu in-degree ile orantılı)
- `network_topN_only.*` — Yalnızca Top N alt-ağ ilişkileri
- `degree_histograms.*` — In/Out-degree dağılımları (log-ölçek)
- `scatter_correlations.*` — In-degree vs Betweenness ve In-degree vs Out-degree saçılımları
- `top10_in_degree.*`, `top10_out_degree.*`, `top10_betweenness.*` — İlk 10 lider listeleri
- `top10_leaders.*` — Bileşik liderlik (BRS) ilk 10
- `top20_risk.*` — En yüksek 20 BRS paketinin çubuk grafiği
- `risk_vs_cascade.*` — BRS ile kaskad etki büyüklüğü ilişkisi (varsa)

### LaTeX tabloları (opsiyonel)
- `metrics_top20_in_degree.tex`, `metrics_top20_out_degree.tex`, `metrics_top20_betweenness.tex`
- `risk_scores_top20.tex`, `edge_betweenness_top10.tex`, `cascade_impact_top20.tex`
- Üretim: `python analysis/make_tables.py`

---

## Öne çıkan bulgular (kısa yorum)
- Ağ yapısı ağır kuyruklu (scale-free) bir dağılım sergiler.
  - Az sayıda “hub” paketin in-degree’i çok yüksektir; bu düğümler ekosistemde omurga rolü oynar.
- İn-degree ile betweenness arasında pozitif bir ilişki gözlemlenir.
  - Popüler (yüksek in-degree) paketler aynı zamanda bilgi akışının kritik boğaz noktalarıdır.
- Bileşik Risk Skoru (BRS), tekil metriklerin ötesinde operasyonel önceliklendirme sağlar.
  - Yüksek BRS, ele geçirilme halinde geniş kaskad etkisi yaratabilecek paketleri işaret eder.
- Kaskad etki (ters yön): Yüksek BRS’ye sahip paketler genellikle daha büyük etki alanına sahiptir; ancak ilişki doğrusal değildir.
  - Komşuluk yapısı farklılıkları, benzer skorlarda farklı yayılım profilleri doğurabilir.

## Sınırlamalar ve Gelecek Çalışmalar
- Betweenness büyük graflarda pahalıdır; örnekleme (SAMPLE_K ≈ 200) ile hızlandırılır.
- Min–max normalizasyon veri kümesine bağlıdır; skorların yorumu bağlama özeldir.
- Gelecek: PageRank/eigenvector entegrasyonu; temporal ağ dinamikleri; topluluk yapılarının risk yayılımına etkisi.

## Daha Fazla Okuma
- Kavramsal arka plan ve geniş rapor: `academic/topolojik-risk-degerlendirmesi.md`
- NPM Yazılım Tedarik Zinciri Saldırıları Raporu: `academic/Readme.md`

## Nasıl yeniden üretilir?
- Yalnızca Notebook: `analysis/analysis.ipynb` dosyasını açın ve hücreleri sırayla çalıştırın.
- Varsayılanlar: `TOP_N = 1000`, örneklemeli betweenness için `SAMPLE_K ≈ 200` önerilir.
- Çıktılar otomatik olarak bu `results/` dizinine yazılır (CSV/JSON + PNG/SVG + .tex).

## Kolay okuma (Python örnekleri)
```python
import csv, json
from pathlib import Path

res = Path('results')

# İlk 10 BRS
rows = list(csv.DictReader((res / 'risk_scores.csv').open(encoding='utf-8')))
rows.sort(key=lambda r: float(r['risk_score']), reverse=True)
top10 = [(r['package'], float(r['risk_score'])) for r in rows[:10]]
print(top10)

# Ağ özet istatistikleri
stats = json.loads((res / 'graph_stats.json').read_text(encoding='utf-8'))
print(stats)
```

## Notlar ve sınırlılıklar
- Büyük graflarda betweenness hesaplaması maliyetlidir; örnekleme (`SAMPLE_K`) önerilir.
- API limitleri/ulaşılabilirliği geçici eksik veri üretebilir; tekrar çalıştırma ve disk önbelleği (`results/cache_deps.json`) yardımcı olur.
- Min–max normalizasyon veri setine bağlıdır; skorların yorumu bağlama özeldir.
