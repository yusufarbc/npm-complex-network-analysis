# Literatür Taraması — NPM Yazılım Tedarik Zinciri Güvenliği (UTF‑8)

Çalışma Tarihi: Ekim 2025

Bu dosya, açık kaynak paket ekosistemlerinde (özellikle NPM) yazılım tedarik zinciri saldırıları (SSCA) alanındaki temel çalışmaları, bulguları ve boşlukları derleyip sentezler. Amaç, ekosistem düzeyinde “önce hangi düğümlere yatırım yapılmalı?” sorusuna giden yolu aydınlatmak ve topolojik risk çerçevesini literatürle ilişkilendirerek güçlendirmektir.

## 1) Genel Arka Plan ve Boşluk Analizi

- Tehdit taksonomileri ve vaka derlemeleri, ekosistemler‑arası kurulum/çalışma zamanı tekniklerini iyi sınıflandırır: Backstabber’s Knife Collection (2015–2019, 174 vaka) ve Hitchhiker’s Guide referans çizgiyi verir; yorumlanan dillerde kayıt suistimali ve kötüye kullanımı ölçen çalışmalar bunu tamamlar.
- NPM odaklı pratik riskler ve fenomenler (Wyss; Kang Yip) detaylandırılmıştır. Ancak bu literatür, “ekosistem düzeyinde hangi düğümlere önce yatırım yapılmalı?” sorusunu doğrudan operasyonel bir önceliklendirmeye dönüştürmez.
- Ağ bilimi cephesinde NPM’nin küçük‑dünya/ölçekten‑bağımsız yapısı ve tekil bakımcı/paketlerin orantısız etkisi açıkça gösterilmiştir (Zimmermann; Hafner; Oldnall). Buna karşın, yapısal/topolojik merkeziyet (derece, betweenness, k‑çekirdek, PageRank) ile kullanım yoğunluğunu (indirme payı, ters‑bağımlı kapsamı) tek bir bileşik “kritiklik” metriğinde birleştiren yaklaşım eksik kalmıştır.
- Bizim katkımız: Son 12 ay indirime dayalı çekirdekte (Top 1000) resmi çözümleme kurallarıyla kurulan yönlendirilmiş graf üzerinde, topolojik ölçüler + kullanım yoğunluğu + bakım/güncellik sinyallerini kaynaştıran Bileşik Kritiklik Skoru (BKS/BRS) ve ona dayalı operasyonel öncelik listeleridir.

## 2) NPM Ağ Topolojisi ve Kırılganlık

- Zimmermann (2019): Az sayıda bakımcı hesabının çoğunluğu etkileyecek kapasitede olduğu; SPOF (tek hata noktası) ve bakım eksikliği etkisi.
- Hafner (2021): Hedefli düğüm çıkarımlarında ağın kırılgan; rastgele hatalarda görece dayanıklı olduğunu niceller; topluluk oluşumları.
- Oldnall (2017): Sürüm düzeyinde beş yıllık NPM topolojisi; küçük dünya + ölçekten bağımsız mimari; 200.000’e varan ters geçişli bağımlılıklar örneği.

Ana mesaj: Hub/omurga düğümlerinin ele geçirilmesi sistemik riski dramatik artırır; bu nedenle ağ‑temelli önceliklendirme gereklidir.

## 3) Bağımlılık Çözümleme ve Yayılım

- Liu ve ark. (ICSE 2022): DVGraph/DTResolver — NPM’nin resmî çözümleme kurallarına sadık, geniş ölçekli (10M+ sürüm, 60M+ ilişki) bilgi grafiği ve geçişli yayılım yolları. DTReme ile giderim.
- Duan ve ark. (2020): Yorumlanan dillerde kayıt istismarı ölçümü; niteliksel çerçeve + meta/statik/dinamik analizle 339 yeni kötü amaçlı paket bildirimi.

Ana mesaj: Doğru çözümleme kuralları, geçişli yayılımı ve etkilerini doğru ölçmek için önkoşuldur.

## 4) Tespit Hattı: ML/Dinamik Analiz ve İmzalar

- Amalfi (2022): ML + reprodüksiyon + klon tespiti; 95 yeni örnek; hafif ve hızlı boru hattı.
- Cerebro (2023): Davranış dizileri ile diller‑arası tespit; NPM/PyPI’de toplam 196+ yeni örnek.
- OSCAR (2024): Sandbox + fuzz + kancalı izlemede güçlü F1; endüstriyel dağıtımda 10.404 NPM, 1.235 PyPI kötü paket.
- ACME (2021): AST kümeleriyle imza üretimi; kümelerden imza çıkarıp kayıt tarama.
- MeMPtec (2024): Metadata temelli; ETM/DTM özellik ayrımı; FP/FN’de yüksek düşüş.
- Cross‑language detection (2023): Dilden bağımsız özelliklerle NPM/PyPI ortak tespit; 58 yeni örnek.

Ana mesaj: Tespit hatları olgunlaşıyor; ancak sınırlı analist kapasitesi için **topolojik bir ön‑filtre** (BRS) ile öncelikli tarama kuyruğu üretmek kritik.

## 5) Bakım/Güncellik ve Operasyonel Sinyaller

- TOOD/PFET (Rahman ve ark., 2024): 2.9M paket, 66.8M sürüm; PyPI genel güncellemede hızlı; Cargo güvenlik düzeltmesi benimsemede önde. TOOD↔PFET ilişkisi.
- Cogo (2020): Downgrade, aynı gün sürümler, deprecation madenciliği; bakım fenomenleri.
- Ahlstrom (2025): Bağımlılık budaması ile lisans/güvenlik risklerinin dramatik azaltımı (%86–94, %57–91).
- Imtiaz (2023): SCA araçları, bildirim gecikmeleri; phantom artifact ve kod inceleme kapsamı (yalnızca %11 tam incelenmiş).

Ana mesaj: Güncellik ve bakım sinyalleri BRS ile birlikte kullanıldığında eyleme dönük **yatırım planları** üretir.

## 6) Politika, İmza ve Bütünlük

- in‑toto (Torres‑Arias, 2020): Uçtan uca bütünlük; zincir adımlarının politikaya uygun kriptografik bağlanması.
- Schorlemmer (2024): İmza benimsemesi; politika etkisi; araçlandırmanın kaliteyi artırması; zorunluluğun miktarı artırması.
- Vaidya (2022): Depo bütünlüğü, commit imzalama, yazılım sertifikasyon hizmeti (SCS), OCI artifaktları için yeknesak sürüm kontrolü.

Ana mesaj: Politika/bütünlük hattı, kayıt yöneticilerinin ve imzalama altyapısının rolünü vurgular; BRS ile **hedef listeleri** bu hattı besler.

## 7) Prototip Kirliliği ve Gizlenme

- Kang Yip (2022): Prototip kirliliği paketlerinin yaygınlığı (%16,8) ve bağımlılık tabanlı istismar.
- Shcherbakov (2021): Dinamik taint ile PP gadget’larının sistematik ortaya çıkarılması; sertleştirme önerileri.

Ana mesaj: Node.js’e özgü zafiyet sınıfları, hub düğümler üzerinde yayılımı büyütebilir; **BRS + sınıf‑özgü tespit** birlikte düşünülmelidir.

## 8) Sentez: Boşluk → Katkı Haritalaması

- Boşluk: Ekosistem düzeyinde operasyonel önceliklendirme ölçütü eksik.
  - Katkı: Bileşik Risk Skoru (BRS) = 0.5·in' + 0.2·out' + 0.3·btw' (min–max), Top 1000 indirime dayalı çekirdek.
- Boşluk: Geçişli yayılım/yüksek hassas çözümleme ile tespit hattı bağlanmıyor.
  - Katkı: Resmî kurallarla kurulan yönlü graf + BRS ön‑filtre → Amalfi/OSCAR/Cerebro için **öncelikli tarama kuyruğu**.
- Boşluk: Politika/bütünlük ve topluluk sağlığı sinyalleri operasyonelleştirilmiyor.
  - Katkı: BRS hedef listeleri + TOOD/PFET + in‑toto/İmza benimsemesi → **hedefli müdahale planları**.

## 9) Seçilmiş Kaynaklar (Kısa Notlarla)

- Backstabber’s Knife Collection (Ohm ve ark., 2020) — 174 gerçek vaka, saldırı ağaçları.
- Hitchhiker’s Guide (Ladisa ve ark., 2023) — 7 ekosistem, 3 kurulum, 5 çalışma zamanı tekniği.
- Zimmermann (2019) — SPOF ve bakımcı merkeziyeti.
- Oldnall (2017) — NPM ağının evrimi, 200K ters bağımlılık örneği.
- Hafner (2021) — Hedefli çıkarıma kırılganlık.
- Liu (ICSE 2022) — DVGraph/DTResolver, DTReme.
- Amalfi (2022), Cerebro (2023), OSCAR (2024), ACME (2021), MeMPtec (2024) — Tespit hattı çalışmaları.
- Rahman (2024), Cogo (2020), Ahlstrom (2025), Imtiaz (2023) — Bakım/güncellik ve SCA ekosistemi.
- Torres‑Arias (2020), Schorlemmer (2024), Vaidya (2022) — Bütünlük ve imza benimsemesi.
- Kang Yip (2022), Shcherbakov (2021) — PP ve sınıf‑özgü tehditler.

---

Bu literatür taraması, ekosistem‑düzeyi risk yönetiminde topolojik merkeziyetin ve kullanım yoğunluğu sinyallerinin birlikte ele alınması gerektiğini; tespit ve politika hatlarına **BRS tabanlı sıralı öncelik listeleri** sağlanmadan sürdürülebilir bir savunmanın zor olduğunu göstermektedir.

