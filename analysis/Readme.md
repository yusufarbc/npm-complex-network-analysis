# 📘 Çalışmanın Özeti

### NPM Ekosisteminde Karmaşık Ağ Analizi

*(Hazırlayan: Yusuf Talha Arabacı – 22 Ekim 2025)*

---

## 🎯 Amaç

Bu çalışma, **JavaScript dünyasının en yaygın paket yönetim sistemi olan NPM** ekosisteminde,
paketlerin **birbirine olan bağımlılıklarından kaynaklanan yapısal riskleri** incelemektedir.

Yani bir paketteki hata, virüs veya kötü niyetli değişikliğin,
**bağımlı olan diğer paketler üzerinden zincirleme şekilde nasıl yayılabileceğini** analiz etmektedir.

Amaç, riskin sadece paketin içinde değil, **paketler arası ilişkilerde** de gizli olduğunu göstermektir.

---

## 🔍 Yaklaşım

Rapor, NPM ekosistemini bir **bağlantı ağı (network)** gibi ele alır:

* Her paket bir **düğüm**,
* Her bağımlılık bir **bağlantı (ok)** olarak temsil edilir.

Bu ağda her paketin “konumu” incelenerek,
**hangi paketlerin ağın omurgasını oluşturduğu** ve **bozulmaları halinde geniş etki yaratabileceği** belirlenmiştir.

Bunun için üç temel ölçüt kullanılmıştır:

1. **In-degree** – Kaç farklı paketin bu pakete bağlı olduğu → “Ne kadar kullanılıyor?”
2. **Out-degree** – Bu paketin kaç farklı bağımlılığı olduğu → “Ne kadar çok şeye bağlı?”
3. **Betweenness** – Ağ içinde köprü olma düzeyi → “İki sistem arasındaki geçit mi?”

Bu üç ölçü birleşerek her paket için bir **“bileşik risk skoru”** oluşturulmuştur.

---

## 📊 Temel Bulgular

### 1. Ekosistem az sayıda “omurga” paket etrafında dönüyor

NPM dünyasında binlerce paket olsa da,
**az sayıda merkezî paket** neredeyse tüm sistemin bel kemiğini oluşturuyor.
Bu paketler çökerse, ekosistemin büyük bölümü etkileniyor.

### 2. En riskli görülen paketler altyapı katmanında

Analiz, özellikle derleme ve test altyapısında yer alan paketlerin
yüksek sistemik risk taşıdığını gösteriyor.

**Öne çıkan kritik paketler:**
`es-abstract`, `tslib`, `@babel/helper-plugin-utils`, `@smithy/types`, `jest-snapshot`, `get-intrinsic`
Bu paketler çoğu projede “arka planda çalışan” ama **çok sayıda başka paketi etkileyen** bileşenlerdir.

### 3. Kaskad etki (zincirleme yayılım) ciddi boyutta

Bazı tekil paketlerdeki bozulma,
**50–80 civarında başka paketi dolaylı olarak etkileyebilir.**
Örneğin `debug` veya `chalk` gibi küçük ama popüler modüller,
görünenden çok daha geniş bir risk alanına sahiptir.

### 4. Ağın kırılganlığı yüksek

Analiz, en kritik birkaç düğümün (paketin) kaldırılması durumunda ağın
**bağlantı bütünlüğünün hızla bozulduğunu** gösteriyor.
Bu da sistemin **fazla merkezileştiğini ve yedekliliğinin düşük** olduğunu kanıtlıyor.

---

## ⚠️ Çıkarımlar ve Öneriler

1. **Yapısal güvenlik izleme** –
   NPM güvenlik stratejileri sadece zafiyet taramasına değil,
   **bağımlılık yapısına (network topolojisine)** de odaklanmalıdır.

2. **Kritik paketlerin öncelikli denetimi** –
   Babel, Jest, TypeScript gibi omurga paketlerin bakım süreçleri
   özel güvenlik politikalarıyla desteklenmelidir.

3. **Tedarik zinciri yönetimi** –
   Geliştiriciler sadece “ne kullandıklarına” değil,
   **“kullandıkları şeylerin neye bağımlı olduğuna”** da dikkat etmelidir.

4. **Ağ temelli risk haritaları** –
   Bu tür analizler düzenli aralıklarla tekrarlanarak,
   risklerin zaman içindeki değişimi izlenmelidir.

---

## 🧠 Sonuç

NPM ekosistemi, **dev bir örümcek ağı** gibidir:
Birkaç ip (paket) ağı ayakta tutar.
Bu iplerden biri koparsa, ağın büyük kısmı dağılır.

Bu nedenle, yazılım güvenliğinde sadece kod kalitesi değil,
**bağımlılık ağının yapısı da** stratejik öneme sahiptir.

---

## 🧭 Genel Amaç

Bu rapor, **NPM (Node Package Manager)** denilen JavaScript dünyasındaki dev kütüphane ekosistemini inceliyor.
Amaç, tek tek paketlerin içeriğine değil, **paketlerin birbirine nasıl bağlı olduğuna** bakmak.
Yani: “Hangi paketler başka hangi paketlere bağımlı?” sorusundan yola çıkarak, bu ağın **yapısal risklerini** ölçüyor.

Bir pakette hata veya saldırı olursa — o pakete bağımlı olan diğerleri de etkilenebilir. Bu zincirleme etkiyi analiz ediyor.

---

## 🧩 Ağ Mantığı (Temel Kavramlar)

Rapor, NPM ekosistemini **yönlü bir ağ (network)** gibi düşünüyor:

* **Düğümler (nodes):** Paketlerin kendisi
* **Bağlantılar (edges):** Bir paketin başka bir pakete bağımlı olması

### 📈 In-degree

Bir pakete **kaç farklı paketin bağlı** olduğunu gösterir.
➡️ Örneğin: 100 farklı paket `lodash`’ı kullanıyorsa, lodash’in in-degree değeri 100’dür.
**Yüksek in-degree** = Bu paket çok merkezî, hata yaparsa birçok şeyi etkiler.

### 📉 Out-degree

Bir paketin **kaç farklı pakete bağımlı** olduğunu gösterir.
➡️ Örneğin: `react-scripts` birçok başka pakete bağlıdır, out-degree değeri yüksektir.
**Yüksek out-degree** = Paket çok şeyden etkilenebilir (bağımlılık yüzeyi geniş).

### 🔀 Betweenness (Aracılık merkeziyeti)

Bir paketin ağ içindeki **köprü rolünü** ölçer.
Eğer iki paket arasındaki yollar genellikle bu paketten geçiyorsa, bu düğüm “boğaz noktası” gibidir.
**Yüksek betweenness** = Kritik köprü; orası çökerse sistemin farklı kısımları birbirinden kopar.

---

## ⚙️ Bileşik Risk Skoru

Bu üç ölçü (in-degree, out-degree, betweenness) **0–1 arasında normalize edilip** bir araya getiriliyor.
Formül basitçe şöyle:

> risk = (in-degree etkisi × 0.5) + (out-degree etkisi × 0.2) + (betweenness etkisi × 0.3)

Böylece her paket için genel bir **“risk puanı”** hesaplanıyor.
Yüksek puan = “Bu paket ekosistemin omurgasında, bozulursa yaygın hasar olur.”

---

## 📊 Grafiklerin ve Tabloların Anlamı

### 1️⃣ **Ağ Görseli (Şekil 1–2)**

* Büyük düğümler: Birçok kişi tarafından kullanılan paketler (yüksek in-degree)
* Renk farkları: En popüler paketlerle diğerlerinin ayrımı
  Bu görselde, **ekosistemin merkezinde yer alan paketlerin** kimler olduğu görülüyor.
  Bu merkezdekiler bir nevi “omurga”.

---

### 2️⃣ **Derece Dağılımı (Şekil 3–4)**

* **Histogramlar (Şekil 3):**
  Çoğu paketin az bağlantısı var ama birkaç tanesi aşırı popüler (örneğin `debug`, `chalk`, `babel`).
  Bu “ağır kuyruklu dağılım”, internetteki birçok doğal sistemde görülür (örnek: sosyal ağlar).
* **Korelasyon grafiği (Şekil 4):**
  Popüler paketler aynı zamanda genellikle köprü görevi de görüyor → “omurga paketler”.

---

### 3️⃣ **Merkeziyet Liderleri (Şekil 5)**

Bu tablo üç farklı açıdan ilk 10 paketi karşılaştırıyor:

* **In-degree liderleri:** Çok kullanılanlar (ör. `tslib`, `@babel/core`)
* **Out-degree liderleri:** Çok şeye bağımlı olanlar
* **Betweenness liderleri:** Ağın “köprü” noktaları

Sonuç: Babel, Jest, TypeScript gibi **derleme ve test altyapısı paketleri** ağın merkezinde.

---

### 4️⃣ **Risk Skoru ve En Riskli Paketler (Şekil 6, Tablo 1)**

Tabloda her paketin:

* Risk puanı
* Kaç kişinin kullandığı (in-degree)
* Kaç pakete bağımlı olduğu (out-degree)
* Köprü rolü (betweenness)
  görülüyor.

En riskli görünenler:
`es-abstract`, `tslib`, `@babel/helper-plugin-utils`, `@smithy/types`, `call-bound`, `jest-snapshot`, `get-intrinsic`...

Yani görünüşte küçük ama ekosistemin derinlerinde **çok bağlantılı** paketler, sistemik risk taşıyor.

---

### 5️⃣ **Kaskad Etkisi (Şekil 7–8, Tablo 2)**

“Kaskad etki”, bir paketteki sorunun **kaç paketi transitif olarak etkileyebileceğini** ölçüyor.
Bazı örnekler:

* `es-errors` → 83 paket etkileniyor
* `debug` → 69 paket etkileniyor
* `chalk` → 40 paket etkileniyor

Grafikte risk puanı ile kaskad etkisi arasında her zaman tam bir paralellik yok —
çünkü ağ yapısı (kim kime bağlı) fark yaratıyor.

---

### 6️⃣ **Köprü Kenarlar (Tablo 3)**

Bazı bağlantılar iki farklı alt sistemi birbirine bağlıyor.
Bunlar koparsa sistem parçalanır.
Örneğin:

* `@jest/transform` ↔ `babel-plugin-istanbul`
* `call-bound` ↔ `get-intrinsic`
  Bu bağlantılar ağın **en kırılgan noktaları**.

---

### 7️⃣ **Ağ İstatistikleri (Tablo 4)**

Genel sayısal özet:

* 1139 paket (düğüm)
* 2164 bağlantı (kenar)
* 160 alt bileşen (küçük bağlantı kümeleri)
* En büyük bileşen 853 paketten oluşuyor
  Yani ağ oldukça **yoğun ama merkezî**, birkaç paket etrafında birleşiyor.

---

## 🔍 Ana Sonuçlar (Basitçe)

* NPM ekosistemi **birkaç kritik pakete çok bağımlı**.
* Bu kritik paketler hem çok kullanılıyor hem de ağın köprüleri.
* Onlardan biri bozulursa, sistemin büyük kısmı etkilenebilir.
* Risk puanları sayesinde hangi paketlerin izlenmesi gerektiği belirlenebilir.
* Ağın “sağlamlık testi”, bu kritik düğümler çıkarılınca bağlantının hızla bozulduğunu gösteriyor.

---

## ⚠️ Sınırlamalar

* Tüm bağımlılıklar dâhil edilmemiş (örneğin “peerDependencies” hariç olabilir).
* Bazı ölçümler tahmini veya örneklemeli.
* Görsellerin düzeni (hangi düğüm nerede duruyor) görsel algoritmalara bağlı.

---

## 🧠 Özetle

Bu rapor şunu söylüyor:

> “NPM dünyası dev bir örümcek ağı gibi.
> Bazı ipler (paketler) çok merkezde ve güçlü.
> Onlardan biri koparsa, ağın büyük kısmı dağılır.”

Yani geliştiriciler için ders şu:

* Sadece güvenli koda değil, **güvenli bağımlılık ilişkilerine** de dikkat etmek gerekir.
* `babel`, `jest`, `tslib` gibi altyapı paketleri düzenli olarak denetlenmeli.

---

# 📘 NPM Karmaşık Ağ Analizi Raporunun Detaylı Açıklaması

---

## 🧠 TEMEL KAVRAMLAR (İstatistik ve Ağ Terimleri)

Bunlar raporda çok geçen teknik ifadeler. Aşağıda her birini günlük dille anlattım 👇

---

### **1️⃣ Düğüm (Node)**

* Her bir “paket” bir düğüm olarak düşünülür.
* Yani `react`, `lodash`, `chalk` gibi her paket ağda bir noktadır.

📍**Basit benzetme:**
Bir sosyal ağdaki kullanıcı gibi — her kullanıcı (düğüm) başka kullanıcılarla bağlantı kurabilir.

---

### **2️⃣ Kenar (Edge)**

* Paketler arasındaki bağlantıdır.
* Eğer A paketi B’ye bağımlıysa, A → B yönünde bir ok (kenar) çizilir.

📍**Benzetme:**
Birinin birine mesaj göndermesi gibi; ok mesajın yönünü gösterir.

---

### **3️⃣ Yönlü Ağ (Directed Graph)**

* Bağlantıların yönü vardır:
  “A, B’ye bağlı” demek, “B, A’ya bağlı” anlamına gelmez.
* Bu yön farkı, “kim kimi kullanıyor?” sorusunu netleştirir.

---

### **4️⃣ In-Degree**

* Bir pakete gelen ok sayısıdır.
* Yani **kaç farklı paket bu pakete bağımlı**.

📈 **Yorum:**
Yüksek in-degree = o paket çok popüler ve birçok kişi onu kullanıyor.
📉 Ancak bu, riskli bir durum da olabilir çünkü bir hatası birçok kişiyi etkiler.

📊 **Grafiklerde:**

* Büyük düğümler genellikle yüksek in-degree’li olanlardır (örneğin `tslib`, `babel`).

---

### **5️⃣ Out-Degree**

* Bir paketten çıkan ok sayısıdır.
* Yani **paket kaç farklı pakete bağımlı**.

📈 **Yorum:**
Yüksek out-degree = paket çok şeyden etkilenebilir.
Bağımlılık yüzeyi geniştir → birinin bozulması onu da bozar.

📊 **Grafiklerde:**

* Bu tür düğümler genellikle “bağımlılığı çok fazla olan” modüllerdir.

---

### **6️⃣ Betweenness Merkeziyeti**

* Ağda iki nokta arasındaki en kısa yolların kaç tanesi bu düğümden geçiyor, onu ölçer.
* Yani bir düğüm “köprü” veya “ara geçiş noktası” mı, bunu gösterir.

📈 **Yorum:**
Yüksek betweenness =
Bu düğüm, ağın farklı bölgeleri arasında bilgi akışını sağlıyor.
Kaybolursa ağ ikiye bölünebilir.

📊 **Grafiklerde:**
Köprü paketler genellikle az bilinen ama yapısal olarak çok önemli modüllerdir (örneğin `get-intrinsic`).

---

### **7️⃣ Bileşik Risk Skoru**

* Tüm bu ölçülerin (in-degree, out-degree, betweenness) birlikte kullanılmasıyla oluşturulmuş tek bir sayı.
* Amaç: Paketleri “karşılaştırılabilir şekilde” sıralamak.

Formül:

> risk = 0.5 × in-degree(normalize) + 0.2 × out-degree(normalize) + 0.3 × betweenness(normalize)

📈 **Yorum:**
Yüksek risk puanı = bu paket hem çok kullanılıyor hem köprü rolü oynuyor hem de geniş bağımlılık ağına sahip.

📊 **Grafiklerde:**
“En riskli 20 paket” tablosu bu hesapla sıralanmış.

---

### **8️⃣ Normalizasyon (Min–Max)**

* Değerlerin hepsi farklı ölçeklerde (örneğin biri 1–100, diğeri 0–0.001).
* Hepsini 0–1 aralığına indirerek eşit ağırlıklı hale getirmek için yapılır.

📉 **Amaç:**
Yüksek sayılar diğerlerini bastırmasın diye “ölçek eşitleme” işlemi.

---

### **9️⃣ Kaskad Etkisi (Cascade Effect)**

* Bir pakette hata çıkarsa, o pakete bağımlı olanlar da etkilenir,
  onlara bağımlı olanlar da…
  Yani **zincirleme etki** oluşur.

📈 **Yorum:**
Kaskad etkisi, bir düğümün dolaylı olarak etkileyebileceği paket sayısını gösterir.
Örneğin bir paket bozulunca 80 tane başka paket hata verebilir.

---

### **🔟 Bileşen (Component)**

* Ağın birbirine bağlı alt grupları.
* Bazı paketler birbirine bağlı değildir, “ayrı küçük adacıklar” oluşturur.

📊 **Zayıf bileşen sayısı:**
Ağda kaç tane bağımsız ada (küme) olduğunu gösterir.
**En büyük bileşen boyutu:**
Birbirine bağlı en geniş grup kaç paket içeriyor?

---

### **11️⃣ Sağlamlık / Robustluk**

* Ağın kritik düğümler silindiğinde ne kadar “ayakta kaldığını” ölçer.

📉 **Yorum:**
Eğer birkaç düğüm çıkarıldığında ağın bağlantısı hızla bozuluyorsa,
bu sistem kırılgandır (robust değil).

---

## 📈 RAPORDAKİ GRAFİKLER VE YORUMLARI

Şimdi rapordaki **her bir görsel ve tabloyu** anlamlı şekilde açıklayalım 👇

---

### **Şekil 1 – Genel Ağ Görseli**

📊 **Ne gösteriyor:**
Tüm Top N (en popüler) paketlerin ve onların bağımlılıklarının oluşturduğu yönlü ağ.
Düğümlerin boyutu “kaç kişi bu paketi kullanıyor”u (in-degree) gösteriyor.
Turuncular Top N paketleri, maviler diğerleri.

💬 **Ne anlama geliyor:**
Orta kısımdaki büyük turuncular ağın “omurgası”.
Bunlar çökerse zincirleme hata oluşur.

---

### **Şekil 2 – Sadece Top N Paketlerin Alt Ağı**

📊 **Ne gösteriyor:**
Yalnızca en popüler paketlerin kendi aralarındaki bağlantılar.

💬 **Yorum:**
Bu alt ağ, popüler paketlerin birbirini nasıl etkilediğini gösterir.
Zincirleme etki burada bile güçlü; popülerler bile birbirine bağımlı.

---

### **Şekil 3 – Derece Dağılımı Histogramları**

📊 **Ne gösteriyor:**

* Solda: Kaç paket kaç bağlantıya sahip?
* Y ekseni log (logaritmik) ölçekli — çünkü dağılım çok dengesiz.

💬 **Yorum:**
Az sayıda devasa bağlantılı paket (örneğin `tslib`, `babel`),
çok sayıda küçük ve yalnız paket var.
Bu tip “ağır kuyruklu” dağılımlar doğada da sık görülür (örneğin sosyal ağlar, internet siteleri).

---

### **Şekil 4 – Korelasyon Grafikleri**

📊 **Ne gösteriyor:**

* Solda: In-degree ile Betweenness ilişkisi
* Sağda: In-degree ile Out-degree ilişkisi

💬 **Yorum:**
Pozitif ilişki var →
Popüler paketler (yüksek in-degree) genellikle ağın köprüsü (yüksek betweenness) konumunda.
Bu da “popüler paket = daha yüksek sistemik risk” demek.

---

### **Şekil 5 – Merkeziyet Liderleri**

📊 **Ne gösteriyor:**
In-degree, out-degree ve betweenness açısından en önde gelen 10 paket.

💬 **Yorum:**

* In-degree liderleri → çok kullanılanlar
* Out-degree liderleri → çok şeye bağımlı olanlar
* Betweenness liderleri → köprü görevi görenler
  Bu üç liste birlikte, riskin hangi açıdan kaynaklandığını gösteriyor.

---

### **Şekil 6 – Bileşik Risk Skoru**

📊 **Ne gösteriyor:**
Tüm metriklerin birleşiminden çıkan toplam risk puanı (0–1 arası).
En riskli 20 paket listesi burada.

💬 **Yorum:**
Liste, görünüşte küçük ama altyapıda kilit rol oynayan paketleri öne çıkarıyor.
Örneğin `es-abstract` veya `tslib` doğrudan fark edilmese de yüzlerce paketi etkiliyor.

---

### **Şekil 7 – Kaskad Etkisi Grafiği**

📊 **Ne gösteriyor:**
Risk puanı en yüksek 20 paketin, hata durumunda kaç paketi dolaylı etkileyebileceği.

💬 **Yorum:**
Kimi zaman küçük risk puanlı paketler bile beklenmedik kadar geniş zincirleme etki yaratabiliyor.
Ağ yapısı karmaşık olduğu için “az riskli” görünen bile tehlikeli olabiliyor.

---

### **Şekil 8 – Risk vs Kaskad Etkisi Saçılım Grafiği**

📊 **Ne gösteriyor:**
Risk puanı ile kaskad etkisi arasındaki ilişki.

💬 **Yorum:**
Doğrusal değil → Yani risk puanı yüksek her paket büyük zincirleme etki yaratmaz.
Bu, ağın bağlantı biçiminin önemini gösteriyor (kim kime bağlı olduğu kadar, nasıl bağlı olduğu da önemli).

---

### **Tablo 3 – Köprü Kenarlar**

📊 **Ne gösteriyor:**
İki paket arasındaki bağlantıların (kenarların) ne kadar köprü görevi gördüğü.

💬 **Yorum:**
Bu bağlantılar koparsa sistem parçalanır.
Örneğin `@jest/transform` ↔ `babel-plugin-istanbul` bağı koparsa, test sisteminin derleme zinciri bozulabilir.

---

### **Tablo 4 – Ağın Temel İstatistikleri**

📊 **Ne gösteriyor:**

* 1139 paket
* 2164 bağlantı
* 160 alt bileşen
* En büyük bileşen: 853 paket
* Ortalama bağlantı sayısı ≈ 1.9

💬 **Yorum:**
Ağ geniş ama merkezî.
Yani birçok paket, birkaç ana düğüm etrafında toplanıyor — merkez çökerse sistem dağılır.

---

## 🧩 Özetle Tüm Bulgular

| Bulgular                                           | Anlamı                                        |
| -------------------------------------------------- | --------------------------------------------- |
| Ağ ağır kuyruklu                                   | Az sayıda güçlü, çok sayıda zayıf paket var   |
| Yüksek in-degree ve betweenness birlikte görülüyor | Popüler olanlar aynı zamanda köprü            |
| Yüksek out-degree                                  | Paket çok bağımlılığa sahip, etkilenmeye açık |
| Bileşik risk skoru                                 | Paketleri genel risk düzeyine göre sıralar    |
| Kritik düğümler silinince ağ parçalanıyor          | Sistem kırılgan, merkezî yapıya bağımlı       |

---

## 🧠 Basit Sonuç

NPM ekosistemi, **çok merkezi ama kırılgan** bir yapıya sahip.
Birkaç kilit paket yüzlercesini birbirine bağlıyor.
Bu nedenle sadece güvenli kod değil, **güvenli bağımlılık ağı** da şart.

---
