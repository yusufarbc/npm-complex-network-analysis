Bu rapor, Node Package Manager (NPM) ekosistemini hedef alan yazılım tedarik zinciri saldırılarına (SSCA) ilişkin önemli olayları, kullanılan vektörleri, kötü amaçlı yazılımın anatomisini ve ekosistemin yapısal kırılganlığını kapsamlı bir şekilde derlemektedir.

---

# NPM Yazılım Tedarik Zinciri Saldırıları Raporu

### 1. Giriş: NPM Ekosisteminin Ölçeği ve Kırılganlığı

Node Package Manager (NPM), modern JavaScript/Node.js geliştirmenin merkezinde yer alan stratejik ve vazgeçilmez bir bileşendir. NPM ekosistemi milyonlarca benzersiz pakete ev sahipliği yapar ve haftalık olarak milyarlarca indirme talebine hizmet vermektedir. Bu devasa ölçek, bir yandan üretkenliği artırsa da, diğer yandan her bir projeyi, kontrolsüz bir şekilde genişleyen geçişli (transitive) bağımlılıklar üzerinden güvenlik risklerine maruz bırakır. Yazılım tedarik zinciri ihlalleri, genel olarak, 2017'den 2019'a kadar %438 artış göstermiştir.

NPM ağı, küçük dünya (small world) davranışı ve ölçekten bağımsız (scale-free) bir mimari sergiler. Bu yapı, az sayıda "hub" (omurga) paketin ele geçirilmesi durumunda tek hata noktaları (SPOF) oluşturarak büyük sistemik risk taşır.

### 2. Önemli NPM Saldırı Olayları ve Vektörleri

Saldırganlar, kötü amaçlı kodlarını ekosisteme sızdırmak için hesap ele geçirmeden yazım hatalarına kadar geniş bir yelpazede vektörler kullanır.

#### 2.1. Otonom Yayılan Solucan Saldırıları: Shai-Hulud (Eylül 2025)

Eylül 2025'te NPM ekosistemini sarsan "Shai-Hulud" solucanı, tedarik zinciri tehditlerinde sistemik bir evrimi temsil eder ve kendi kendini kopyalama (self-replicating) yeteneğine sahip wormable bir tehdittir.

• Saldırı Vektörü (Phishing): Saldırı, NPM paket bakımcılarını hedefleyen organize bir kimlik avı (phishing) kampanyasıyla başladı. Saldırganlar, bakımcıların Çok Faktörlü Kimlik Doğrulama (MFA) sıfırlama sahteciliği için npmjs.help gibi sahte alan adlarını kullanarak kimlik bilgilerini çaldı.
• Kapsam ve Etki: Saldırı, chalk, debug ve @ctrl/tinycolor (haftalık 2.2 milyon indirme) dahil olmak üzere 18 pakette başladı ve hızla 500'den fazla NPM paketini etkiledi. Etkilenen paketlerin haftalık indirme sayısı 2.6 milyarı (chalk/debug) aştı.
• Payload ve Yayılım: Solucan, ele geçirdiği NPM token'larını kullanarak meşru paketlerin tarball'unu indirip, package.json dosyasını değiştirip kötü amaçlı bir betik (bundle.js) enjekte ederek paketi yeniden yayınladı (NpmModule.updatePackage). Malware, bulut hizmeti token'larını (örn. AWS, GCP) çalmak ve Trufflehog gibi meşru güvenlik araçlarını taklit ederek gizli kimlik bilgilerini taramak üzere tasarlanmıştır.
• LLM Kullanımı: Bir Büyük Dil Modeli'nin (LLM) kötü amaçlı kodun yazılmasına yardımcı olmak için kullanıldığı orta düzeyde bir güvenle değerlendirilmektedir.
• Sonuç: Saldırı sonucunda 2.349 kimlik bilgisi (GitHub PAT'leri, cloud keys vb.) sızdırıldı. Wiz telemetry, 500 özel deponun (private repo) herkese açık hale getirildiğini rapor etmiştir.

#### 2.2. CI/CD Altyapı Ele Geçirme: Nx / S1ngularity (Ağustos 2025)

Nx paketlerini hedef alan bu olay, Shai-Hulud saldırısının doğrudan öncülü olarak görülmektedir.

• Vektör: Saldırganlar, bir GitHub Actions injection zafiyetini istismar ederek NPM yayınlama token'ını çaldı.
• Eylem: Çalınan token ile Nx'in meşru paketlerinin kötü amaçlı sürümleri 4 saat boyunca yayınlandı. Kötü amaçlı kod, kullanıcı sistemlerini hassas veriler için tarayıp bunları herkese açık GitHub depolarına yüklüyordu.
• Yanıt: Nx, saldırı sonrası NPM Trusted Publishers (Güvenilir Yayıncılar) mekanizmasını uygulayarak token tabanlı kimlik doğrulamadan kaçınmayı hedeflemiştir.

#### 2.3. Yüksek Profilli Hesap Ele Geçirme ve Paket Devri

• UAParser.js (2021): Çok sayıda büyük teknoloji şirketi tarafından kullanılan bu paket, bir bakımcının ele geçirilmiş hesabı aracılığıyla kötü amaçlı kod içerecek şekilde değiştirildi. Amaç, coinminer kurmak ve kullanıcı/kimlik bilgilerini toplamaktı.
• event-stream (2018): Bu popüler paket, sosyal mühendislik yoluyla kötü niyetli bir aktöre devredildi ve yeni bakımcı pakete kripto cüzdanlarını hedefleyen yük ekledi.
• eslint-scope (2018): Hesap ele geçirmeye dayalı, geliştirici kimlik bilgilerinin çalındığı bir olay.
• chalk/debug (Eylül 2025): Shai-Hulud'un ilk aşamasında 18 pakete kripto hırsızı yükü enjekte edildi.

#### 2.4. Sosyal ve İsimlendirme Saldırıları

• Typosquatting: cross-env yerine crossenv gibi benzer isimlerle kötü amaçlı paketler yayınlanır.
• Dependency Confusion: Dahili paket adıyla aynı addaki herkese açık kötü niyetli paket, daha yüksek sürüm numarasıyla yayınlanır ve paket yöneticisi tarafından tercih edilir.

#### 2.5. Gizli ve Yapısal Zafiyetler

• Kötü Amaçlı Kurulum Komutları: Kötü amaçlı paketlerin %81'i post-install/pre-install betiklerini kullanır.
• Shrinkwrapped Klonlar: Yamalanmış açıklar taşıyan klonlar, npm audit ile gözden kaçabilir.
• Süresi Dolmuş Alan Adları: 601’e yakın alan adının devralmaya açık olabileceği tahmin edilmektedir.
• Prototip Kirliliği: Node.js’e özgü; uzaktan kod çalıştırmaya kapı aralayabilir.
• Hayalet Eserler: Kayıt defterine yüklenen kodun depoda yer almaması; popüler güncellemelerin %20.1’inde gözlenmiştir.

### 3. NPM Ağının Yapısal Kırılganlığı ve Risk Analizi

• Ağ modeli: Düğümler paket; kenarlar Bağımlı → Bağımlılık (yönlü).
• Ölçüler: In-degree (yayılım potansiyeli), Betweenness (köprü/boğaz noktası).

### 4. Bileşik Risk Skoru (BRS)

• Normalize edilmiş merkeziyet ölçülerinin ağırlıklı toplamı: risk = 0.5·in' + 0.2·out' + 0.3·btw'.
• Kritik paketler (örnek): es-abstract, tslib, @babel/helper-plugin-utils.
• Kaskad etki: Yüksek riskli düğümlerin ters yöndeki etkisi büyüktür (ör. es-errors: 83).

### 5. Kötü Amaçlı Yazılımın Anatomisi ve Gizlenme Taktikleri

• Hedefler: Bulut token’ları, kimlik bilgileri, cüzdanlar.
• Gizleme: Base64/hex kodlama; LLM tabanlı tespitlere karşı “false negative engineering”.
• Parser Confusion: SBOM’da görünmez kılma için bildirimin manipülasyonu.

### 6. Savunma ve Tespit Mekanizmaları

• Otomatik Tespit: Cerebro (davranış dizileri), OSCAR (dinamik analiz), Amalfi (ML + reprodüksiyon + klon tespiti), LATCH (kurulum sandbox’ı).
• Proaktif Çerçeve: in-toto (uçtan uca tedarik zinciri bütünlüğü).

---

### Sonuç

Saldırılar, rastgele istismardan hesap ele geçirme ve otonom yayılma gibi sistemik tehditlere evrilmiştir. Savunma, SCA’nın ötesinde proaktif bütünlük doğrulaması ve davranışsal/LLM tabanlı tespitleri içeren çok katmanlı bir stratejiye dönüşmelidir. Topolojik merkeziyet kullanılarak hesaplanan BRS, sınırlı analist kapasitesini yüksek etki potansiyeline sahip düğümlere yönlendiren pratik bir önceliklendirme aracıdır.
