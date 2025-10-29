## results/ — Üretilen çıktılar

Amaç
- Analiz sürecinin ürettiği veri dosyaları, görseller ve LaTeX tablolarını barındırır.
- `index.html` ve `academic/` altındaki raporlar bu klasörden beslenir.

Önemli Dosyalar
- `edges.csv` — Kenar listesi (source=dependent, target=dependency)
- `metrics.csv` — `package,in_degree,out_degree,betweenness,is_topN`
- `risk_scores.csv` — Bileşik risk skorları ve metrikler
- `graph_stats.json` — Genel ağ istatistikleri (düğüm/kenar, bileşenler, LCC çapı mümkünse)
- `top_packages.txt` — Analizde kullanılan Top N paket isimleri
- `edge_betweenness_top10.csv` — En yüksek köprü kenarlar
- `cascade_impact_top20.csv` — Ters yön (dependents) kaskad etkisi
- `classification.csv` — (opsiyonel) kantil tabanlı risk sınıflandırması
- Görseller — `*.png/.svg` (ağ, histogram/korelasyon, liderler, kaskad etkisi)
- Tablolar — `*.tex` (LaTeX uzun tablolar; `analysis/make_tables.py` ile üretilir)

Kullanım
- Görseller ve tablolar `index.html` ve LaTeX raporunda doğrudan referanslanır.
- LaTeX tablolarını güncelle: `python analysis/make_tables.py`

Notlar
- Yeniden çalıştırmalarda mevcut dosyalar üzerine yazılır.
- Büyük görseller için SVG tercih edilir (daha keskin çıktı, daha küçük depo boyutu).

