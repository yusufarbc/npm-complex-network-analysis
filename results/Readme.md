## results/ – Üretilen çıktılar

Amaç: Analiz not defterlerinin ürettiği veri dosyaları, görseller ve LaTeX tablolarını içerir. `index.html` ve `academic/` altındaki raporlar bu klasörden beslenir.

İçerik (önemli dosyalar)
- `edges.csv` – Kenar listesi (source=dependent, target=dependency)
- `metrics.csv` – `package,in_degree,out_degree,betweenness,is_topN`
- `risk_scores.csv` – Bileşik risk skorları ve metrikler
- `robustness_risk.json` – Genel ağ istatistikleri (düğüm/kenar, bileşenler, vb.)
- `top_packages.txt` – Analizde kullanılan Top N paket isimleri
- Görseller – `*.png/.svg` (ağ görselleri, histogram/korelasyon, liderler, kaskad etkisi)
- Tablolar – `*.tex` (LaTeX uzun tablo çıktıları; `make_tables.py` ile üretilir)

Kullanım
- Görseller ve tablolar `index.html` ve LaTeX raporunda doğrudan referanslanır.
- LaTeX tablolarını güncelle: `python results/make_tables.py`

Bağımlılıklar
- Yok (sadece üretilmiş dosyalar). `make_tables.py` için Python gerekir.

Notlar
- Yeniden çalıştırmalarda mevcut dosyalar üzerine yazılır.
- Büyük görseller için SVG tercih edilir (daha keskin çıktı, daha küçük repo boyutu olabilir).

