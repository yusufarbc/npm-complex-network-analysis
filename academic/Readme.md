# Literatür Tablosu - TR

| **Makale Adı (Kısa Başlık)**                                                                                      | **Yazarlar**                                 | **Yıl** | **Kaynak Türü (Dergi/Konferans)** | **Anahtar Kelimeler**                                                                                               | **Problem**                                                                                                | **Yöntem / Mimari**                                                                                          | **Veri Seti / Deney Ortamı**                                           | **Temel Bulgular / Katkı**                                                                                                                                | **Zayıf Yönleri / Sınırlılıklar**                                                                       | **Tezimle İlgisi / Notlar**                                                                                                 | **Durum**     |
| ----------------------------------------------------------------------------------------------------------------- | -------------------------------------------- | ------- | --------------------------------- | ------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------- | ------------- |
| **The Web of Dependencies: A Complex Network Analysis of the NPM**                                                | Emilie-Rose Oldnall                          | 2017    | Tez (Yüksek Lisans Tezi)          | npm, dependency network, JavaScript, open-source, network complexity, small-world behavior, scale-free architecture | Npm ağının topolojik özelliklerinin incelenmesi ve düğüm arızasının ağ üzerindeki yayılımının simülasyonu. | Karmaşık Ağ Analizi (CNA), Betweenness Centrality, Ağ Kırılganlığı Simülasyonları.                           | 2017 yılına ait NPM paket bağımlılık verileri.                         | Ağın, hedefli saldırılarda kritik düğümlerin çıkarılmasıyla hızla parçalanan (kırılgan) bir yapıya sahip olduğu.                                          | Nicel bir Bileşik Risk Skoru yok; kaskad etki mekanizması basittir.                                     | TEMEL: Kırılganlık ve CNA metodolojisini destekler.                                                                         | Yüksek Benzer |
| **Small World with High Risks: A Study of Security Threats in the npm Ecosystem**                                 | Zimmermann, M., Staicu, C., et al.           | 2019    | Konferans (USENIX Sec 2019)       | Centrality measure, Node detection, Optimization, Network security                                                  | Az sayıda paket/bakımcı üzerinden ekosistem ölçeğinde güvenlik risklerinin incelenmesi.                    | Bağımlılık Grafiği, Transitive Reach (Geçişli Erişim) ve Bakımcı analizi.                                    | 676K paket, 199K bakımcı (2018'e kadar).                               | SPOF Kanıtı: Az sayıda bakımcının ekosistemin %50'den fazlasına ulaşabildiği; %40'ın üzerinde paketin bilinen açıklarla yaşadığı.                         | Top 1000 alt kümesine odak yok; Merkeziyet metrikleri sınırlı kullanılıyor.                             | YÜKSEK BENZER: Merkeziyetin güvenlik riskiyle ilişkisini kuran temel literatürdür.                                          | Yüksek Benzer |
| **Node Package Manager’s Dependency Network Robustness**                                                          | Hafner, A., Mur, A., Bernard, J.             | 2021    | Yayın Öncesi (arXiv Preprint)     | npm, dependency network, robustness, targeted attacks, software resilience                                          | Npm ekosisteminin kritik paketlere yapılan hedefli saldırılara karşı kırılganlığı.                         | Yönlü Graf Modellemesi; Hata Simülasyonları (rastgele, hub, PageRank); LCC (En Büyük Bağlı Bileşen) analizi. | Tüm NPM Kayıt Defteri (~1.7M paket, 2012-2021 arası anlık görüntüler). | Kırılganlık: Ağın hedefli saldırılara karşı dayanıksız olduğu (%60-90 kesinti); güç yasası dağılımı. Merkezi paketlerin kendi bağımlılıklarını azalttığı. | Top 1000 alt kümesine spesifik odak yok. Simülasyonlar sınırlı kaldırım oranlarında yapılmış.           | TEMEL ÖNCÜL: Robustluk ve CNA metodolojisinin güvenlik için kullanımını kanıtlar. Projemizin metodolojik başlangıç noktası. | Yüksek Benzer |
| **On the Impact of Security Vulnerabilities in the npm Dependency Network**                                       | Decan, A., Mens, T., et al.                  | 2018    | Konferans (MSR 2018)              | Software repository mining, Security vulnerability, Dependency network, Semantic versioning                         | NPM'de raporlanan zafiyetlerin bağımlılık ağında nasıl yayıldığı ve giderildiği.                           | Ampirik analiz; Snyk veritabanı ile açıkların yayılım ve düzeltme süreçlerinin incelenmesi.                  | ~610K paket, ~400 güvenlik raporu.                                     | Zafiyetlerin yüzbinlerce sürümü etkilediği; açık bildirim/düzeltme sürecinin yavaş olduğu.                                                                | Merkeziyet metrikleri (Betweenness/PageRank) doğrudan kullanılmadı; sadece mevcut açık verisine odaklı. | KISMİ: NPM bağımlılık ağı + güvenlik ilişkisi var; ancak metodoloji (merkeziyet/density) farklıdır.                         | Kısmi         |
| **Towards Using Package Centrality Trend to Identify Packages in Decline**                                        | Mujahid, S., Serebrenik, A.                  | 2021    | Dergi (IEEE Trans. Eng. Manag.)   | Package centrality, Decline detection, Dependency graph, npm                                                        | Paketlerin merkeziyet (PageRank) değişimiyle popülerlik/kullanımdan kalkış düşüşünü öngörmek.              | Aylık PageRank hesaplayarak trend analizi ve doğrusal regresyon.                                             | NPM ekosistemi verileri (aylık network snapshotları).                  | Merkeziyet sıralamasındaki tutarlı düşüşün, paketlerin gelecekteki popülerlik kaybını güçlü bir şekilde öngördüğü.                                        | Güvenlik veya tedarik zinciri bağlamı yok; sadece popülerlik tahmini.                                   | KISMİ: Merkeziyet metriğini (PageRank) zaman içinde kullanması metodolojik açıdan benzer.                                   | Kısmi         |
| **Demystifying Vulnerability Propagation via Dependency Trees in npm**                                            | Liu, C., Chen, S., et al.                    | 2022    | Konferans (ICSE 2022)             | Vulnerability propagation, Dependency trees, npm, Security, Knowledge graph                                         | Bağımlılık ağaçlarındaki hatalı çözümlemelerin zafiyet yayılım yollarını gizlemesi.                        | Bilgi Grafiği (DVGraph); Ağaç tabanlı çözümleme ile ampirik çalışma.                                         | 10M versiyon, 60M bağımlılık.                                          | Zafiyetlerin bağımlılık ağaçlarında şiddetlendiği; ekosistem çapında tehditler olduğu.                                                                    | Odaklanma yayılıma; tam merkeziyet/density analizi eksik.                                               | YÜKSEK BENZER: NPM + dependency analysis + supply chain security; Ağacı, ağ yapısının bir varyantı olarak kullanır.         | Yüksek Benzer |
| **On the Impact of Security Vulnerabilities in the npm and RubyGems Dependency Networks**                         | Zerouali, A., Mens, T., et al.               | 2022    | Dergi (Empirical Software Eng.)   | Security vulnerabilities, npm, RubyGems, Package manager security                                                   | NPM ve RubyGems'teki açıkların açıklanma, yayılma ve fark edilme sürelerini karşılaştırmak.                | Karşılaştırmalı ampirik çalışma; Snyk veri tabanı ile açıkların evrimi ve yayılım analizi.                   | NPM/RubyGems paketleri ve zafiyet veri tabanları.                      | NPM'de açık sayısı artıyor; dış projelerin %33'ü, paketlerin %40'ı hala açık paketler içeriyor.                                                           | Karşılaştırmalı, NPM'e özel değil. Merkeziyet analizine yer verilmedi.                                  | KISMİ: NPM ağ güvenliğini ele alıyor; ancak derinlemesine ağ metriği analizi eksik.                                         | Kısmi         |
| **Towards Sustainable and Secure Reuse in Dependency Supply Chains**                                              | Reid, B., Kula, R.                           | 2025    | Atölye (SE in 2030 Workshop)      | Software ecosystems, Dependency supply chains, Security, Sustainable reuse                                          | Bağımlılık zincirinin sonunda bağımlılığı olmayan (end-of-chain) npm paketlerini incelemek.                | Örnek vakalarla ve popüler zincir analiziyle end-of-chain paketlerinin rolünü analiz etme.                   | NPM üst paketlerinden alt bağımlılık zincirleri (örnek vaka odaklı).   | Popüler zincirlerin %50’den fazlasının bağımlılığı olmayan "end-of-chain" paketlerden oluştuğu.                                                           | Ağ metriği veya sayısal analiz yok; vaka ve tasarım odaklı.                                             | KISMİ: Güvenlik değil, sürdürülebilir yeniden kullanım perspektifi var.                                                     | Kısmi         |
| **Structural and Connectivity Patterns in the Maven Central Software Dependency Network**                         | Pothula, G. K., et al.                       | 2025    | Yayın Öncesi (arXiv)              | Maven Central, Software dependencies, Dependency analysis, Network security                                         | -                                                                                                          | -                                                                                                            | -                                                                      | -                                                                                                                                                         | -                                                                                                       | -                                                                                                                           | -             |
| **VulRG: Multi-Level Explainable Vulnerability Patch Ranking for Complex Systems Using Graphs**                   | NAY OO, NCS Cyber Special Ops R&D, Singapore | 2025    | Yayın Öncesi (arXiv)              | Vulnerability prioritization, Patch ranking, Cybersecurity, Graph-based framework                                   | -                                                                                                          | -                                                                                                            | -                                                                      | -                                                                                                                                                         | -                                                                                                       | -                                                                                                                           | -             |
| **Predicting Nodal Influence via Local Iterative Metrics**                                                        | Shilun Zhang, Alan Hanjalic, Huijuan Wang    | 2024    | Dergi (Scientific Reports)        | Nodal influence, Centrality metrics, Network prediction, Iterative metrics                                          | Düğüm etkisini tahmin etme, yerel ve küresel topolojik bilgileri birleştirme.                              | Yinelemeli metrikler ile düğüm etkisi tahmini; regresyon modeli.                                             | Çeşitli gerçek ve sentetik ağlar.                                      | Yinelemeli metriklerin K=4 ile en iyi performansı gösterdiği; düşük karmaşıklık ile yüksek doğruluk sağlandığı.                                           | Ağlar için karmaşıklık ve bilgi gereksinimlerini dengeleme zorunluluğu.                                 | Yüksek Benzer: Küresel ve yerel metriklerin kombinasyonu ve tahminleme metodolojisi.                                        | Yüksek Benzer |
| **Securing Network Resilience: Leveraging Node Centrality for Cyberattack Mitigation and Robustness Enhancement** | Essia Hamouda, Mohsen ElHafsi, Joon Son      | 2024    | Akademik Rapor (Springer)         | Network security, Node centrality, Cyberattack mitigation, Optimization                                             | Kritik düğüm analizi ve ağ dayanıklılığı artırma.                                                          | Merkeziyet skoru kullanılarak kaynak tahsisi ve saldırı riski minimizasyonu.                                 | Çeşitli ağlarda güvenlik ölçümleri ve simülasyonlar.                   | Merkeziyet kullanarak siber saldırı risklerini azaltan bir model önerilmektedir.                                                                          | Yüksek hesaplama maliyetleri ve kaynak tahsisi gereksinimleri.                                          | Yüksek Benzer: Kritik düğüm analizi ve kaynak tahsisi.                                                                      | Yüksek Benzer |

---

# Literatür Araştırması - TR

---

## 1. Bağımlılıkların Ağı: NPM’de Karmaşık Ağ Analizi

### Özet

Açık kaynak yazılım geliştirme, yazılım paketleri arasında karmaşık bağımlılıklar yaratan işbirlikçi bir çabadır. Tescilli yazılımların aksine, açık kaynak modeli, bağımlılıkları analiz etme ve izleme fırsatı sunar. Bu tez, JavaScript için paket yöneticisi olan npm ekosistemindeki karmaşık bağımlılık ağını haritalandırmaktadır. JavaScript, dünyadaki en yaygın kullanılan programlama dilidir ve paket yöneticisi, geliştirici topluluğuna binlerce üçüncü taraf yazılım paketini depolamak ve dağıtmakla sorumludur. Ancak, artan bağlantılılık, aynı oranda artan bir güvenlik açığı da getirir; 2016 yılında küçük bir yardımcı paket olan *left-pad*'ın npm kaydından kaldırılması, birçok yazılım uygulamasının beklenmedik bir şekilde çalışmasını engellemiştir.
Bu tez, ağ ölçütlerinin npm ağının yapısını ve karmaşıklığını belirlemek için nasıl kullanılabileceğini ve bu parametrelerin zamanla nasıl evrildiğini gösterir. Npm ağı, küçük-dünya davranışı ve ölçek serbest mimari sergileyerek, mevcut açık kaynak yazılım sistemleri üzerine yapılan çalışmaları doğrular. Tez, ağın işlevselliğini orantısız şekilde etkileyen versiyonlanmış paketleri tanımlar ve merkezi düğümlerin 200.000'e kadar ters transitif bağımlılığa sahip olabileceğini, bu da ekosistemin zincirleme arızalara karşı duyarlılığını vurgular.

### Anahtar Kelimeler

npm, bağımlılık ağı, JavaScript, açık kaynak, ağ karmaşıklığı, küçük-dünya davranışı, ölçek serbest mimari

---

## 2. Küçük Dünya, Yüksek Riskler: npm Ekosistemindeki Güvenlik Tehditlerinin Bir İncelemesi

### Özet

Ağ saldırıları ve siber güvenlik alanındaki dinamik ve sürekli değişen manzaraya yanıt olarak, bu çalışma, ağ güvenliğini iyileştirmeyi amaçlayarak kritik düğümleri belirleyip, kaynak tahsisini bütçe kısıtlamaları içinde optimize etmeyi hedeflemektedir. Dört yaygın olarak tanınan merkeziyet ölçüsünden elde edilen düğüm merkeziyet puanlarını kullanarak, ağ saldırısı olasılıklarını belirlemek için alışılmadık ancak etkili bir yaklaşım önerilmektedir. Ayrıca, düğüm odaklı özellikler ve saldırı olasılıkları ile ağ dayanıklılığını ilişkilendiren kapalı formda bir ifade önerilmektedir. Bu yaklaşım, kaynak tahsisi stratejilerini belirleyerek kritik düğümler üzerindeki siber saldırı risklerini minimize ederken ağın dayanıklılığını artırmayı sağlar. Sayısal sonuçlar, yaklaşımımızın doğruluğunu doğrulamaktadır ve yeni güvenlik tehditlerine karşı dayanıklılığın iyileştirilmesine katkıda bulunmaktadır.

### Anahtar Kelimeler

Merkeziyet ölçüsü, Düğüm tespiti, Performans değerlendirmesi, Optimizasyon, Ağ güvenliği

---

## 3. Node Package Manager’ın Bağımlılık Ağı Dayanıklılığı

### Özet

Npm bağımlılık ağının dayanıklılığı kritik bir özelliktir çünkü birçok proje, özellikle birçok bağımlı paketi olan popüler paketlerin işlevselliklerine büyük ölçüde dayanır. Geçmişte, bazı npm paketlerinin kaldırılması veya güncellenmesi, internet üzerinde geniş çapta kaosa ve web sayfalarının zaman zaman çalışmamasına neden olmuştur. Bu çalışmanın amacı, ağın bu tür durumlardaki dayanıklılığını zaman içinde izlemektir. Çalışma, ağın hedeflenmiş saldırılara karşı dayanıklı olmadığını göstermekte ve önemli düğümlerdeki bir güvenlik riskinin ağın büyük bir kısmını etkileyeceğini ortaya koymaktadır. Ancak, bu durum, güçlü topluluklar tarafından desteklenen paketler sayesinde önemli bir endişe yaratmamaktadır ve ağın güç yasası dağılımı nedeniyle doğal bir sonuçtur. Ortalama bağımlılık sayısının ve önemli düğümlerin ağ üzerindeki etkisinin azaldığı mevcut trend, dayanıklılığı artırmakta ve gelişim için olumlu bir yol göstermektedir.

### Anahtar Kelimeler

npm, bağımlılık ağı, dayanıklılık, hedeflenmiş saldırılar, yazılım dayanıklılığı

---

## 4. npm Bağımlılık Ağındaki Güvenlik Açıklarının Etkisi

### Özet

Güvenlik açıkları, açık kaynak yazılım paket kütüphanelerindeki en önemli problemlerden biridir. Bu makale, npm bağımlılık ağında altı yıl süresince 400'e yakın güvenlik raporunu incelemektedir. Güvenlik açıklarının ne zaman keşfedildiği, düzeltildiği ve bunların bağlı paketler üzerindeki etkilerini analiz eder. Ayrıca, bu açıkların bağımlılık kısıtlamaları ve bağımlı paketler üzerinde nasıl yayıldığını incelemektedir. Çalışma, paket bakımcıları ve araç geliştiricilerinin güvenlik problemleriyle başa çıkma süreçlerini iyileştirmelerine yönelik yönergeler sunmaktadır.

### Anahtar Kelimeler

Yazılım deposu madenciliği, Güvenlik açığı, Bağımlılık ağı, Semantik sürümleme

---

## 5. Paket Merkeziyet Eğilimi Kullanarak Gerileyen Paketleri Tanımlamaya Yönelik Bir Yöntem

### Özet

Günümüz yazılım sistemleri, giderek daha fazla yeniden kullanılabilir kod ve paketlere dayalı olarak geliştirilmekte olup, bu yazılım ekosistemleri hızla evrimleşmektedir. Bu makale, npm ekosisteminde merkezîyet eğilimlerini kullanarak gerileyen paketleri tanımlamak için ölçeklenebilir bir yaklaşım önermektedir. Bu yaklaşım, merkeziyet eğilimlerini izleyerek paketlerin topluluk ilgisini kaybettiği zamanları doğru bir şekilde tahmin edebilmekte ve mevcut popülerlik metriklerinden 18 ay önce gerileyen paketleri tespit edebilmektedir.

### Anahtar Kelimeler

Paket merkeziyeti, Gerileme tespiti, Bağımlılık grafiği, npm

---

## 6. npm Bağımlılık Ağaçlarında Güvenlik Açığı Yayılımını Açıklığa Kavuşturma

### Özet

Üçüncü taraf kütüphaneler, JavaScript yazılımının hızlı bir şekilde geliştirilmesine olanak sağlar, ancak aynı zamanda güvenlik tehditlerini de beraberinde getirir. Bu makale, npm ekosisteminde bağımlılık ağaçları aracılığıyla güvenlik açıklarının nasıl yayıldığını incelemektedir. Çalışma, 10 milyonun üzerinde kütüphane versiyonu ve 60 milyon bağımlılık ilişkisini kapsayan bir bilgi grafiği kullanarak, güvenlik tehditlerini büyük ölçekli bir şekilde takip etmekte ve çözüm önerileri sunmaktadır.

### Anahtar Kelimeler

Güvenlik açığı yayılımı, Bağımlılık ağaçları, npm, Güvenlik, Bilgi grafiği

---

## 7. npm ve RubyGems Bağımlılık Ağı Güvenlik Açıklarının Etkisi

### Özet

Bu çalışma, npm ve RubyGems gibi iki büyük açık kaynak yazılım ekosistemindeki güvenlik açıklarını karşılaştırmaktadır. Güvenlik açıklarının ne zaman ve nasıl açıklanıp düzeltildiğini ve bağımlı paketlerin nasıl etkilendiğini incelemektedir. Ayrıca, açık kaynak yazılım paket dağıtımlarının güvenliğini iyileştirmek için yapılması gerekenlere dair bulgular sunmaktadır. npm'deki güvenlik açıklarının arttığı ve daha hızlı bir şekilde açıklandığı gözlemlenmiştir.

### Anahtar Kelimeler

Güvenlik açıkları, npm, RubyGems, Paket yöneticisi güvenliği

---

## 8. Bağımlılık Tedarik Zincirlerinde Sürdürülebilir ve Güvenli Yeniden Kullanım

### Özet

Bu makale, bağımlılık zincirlerinin sonunda yer alan ve dış bağımlılıkları olmayan paketleri incelemektedir. Bu tür paketler, bağımlılıklardan kaynaklanan risklerden kaçınmakta olup, yazılım yeniden kullanımında güvenlik ve sürdürülebilirlik için önemli dersler sunmaktadır.

### Anahtar Kelimeler

Yazılım ekosistemleri, Bağımlılık tedarik zincirleri, Güvenlik, Sürdürülebilir yeniden kullanım

---

## 9. Maven Central Yazılım Bağımlılık Ağı Yapısı ve Bağlantı Desenleri

### Özet

Bu makale, Java kitaplıklarının en büyük depolarından biri olan Maven Central ekosistemini analiz etmektedir. Bağımlılık ağını ağ bilimi teknikleriyle inceleyen çalışma, ağdaki merkezi düğümlerin sistemik riskler oluşturduğunu ve bu düğümlerdeki hataların tüm ekosistemde zincirleme etkiler yaratabileceğini ortaya koymaktadır.

### Anahtar Kelimeler

Maven Central, Yazılım bağımlılıkları, Bağımlılık analizi, Ağ güvenliği

---

## 10. VulRG: Karmaşık Sistemler İçin Çok Seviyeli Açıklanabilir Güvenlik Açığı Yama Sıralaması

### Özet

Bu çalışma, karmaşık sistemlerde güvenlik açıklarını önceliklendirmek için yeni bir grafik tabanlı çerçeve sunmaktadır. Ağ iletişimi ve sistem bağımlılığı grafikleri kullanılarak riskler değerlendirilmekte ve siber tehditler azaltılmaktadır. Çalışma, mevcut yöntemlere kıyasla daha doğru sonuçlar elde etmektedir.

### Anahtar Kelimeler

Güvenlik açığı önceliklendirme, Yama sıralaması, Siber güvenlik, Grafik tabanlı çerçeve

---

## 11. Yerel Yinelemeli Ölçütler Kullanarak Düğümsel Etkiyi Tahmin Etme

### Özet

Bu çalışma, düğümlerin etkisini daha iyi tahmin edebilmek için yerel ve küresel topolojik bilgileri birleştirmenin etkisini araştırmaktadır. Yinelemeli metrikler önererek, ağdaki düğümün etkisini giderek daha fazla küresel bilgi ile tahmin etmektedir.

### Anahtar Kelimeler

Düğüm etkisi, Merkeziyet ölçütleri, Ağ tahmini, Yinelemeli metrikler

---

## 12. Ağ Dayanıklılığını Güvenceye Alma: Siber Saldırıları Azaltmak İçin Düğüm Merkeziyeti Kullanma

### Özet

Bu çalışma, ağ güvenliğini artırmak için düğüm merkeziyet puanlarını kullanarak kritik düğümleri belirlemeyi ve kaynak tahsisini optimize etmeyi amaçlamaktadır. Optimizasyon teknikleri kullanılarak, siber saldırı risklerini azaltmak ve ağ dayanıklılığını artırmak için yeni bir yaklaşım önerilmektedir.

### Anahtar Kelimeler

Ağ güvenliği, Düğüm merkeziyeti, Siber saldırı azaltma, Optimizasyon

---

Tabii! İşte orijinal İngilizce haliyle düzenlenmiş metin:

---

# Literature Review - EN

---

## 1. The Web of Dependencies: A Complex Network Analysis of the NPM

### Abstract

Open-source software development is a collaborative effort resulting in complex dependencies between software packages. Unlike proprietary software, the open-source model offers a unique opportunity to analyze and trace these dependencies due to its public availability. This thesis maps out the complex dependency network within the npm ecosystem, the package manager for JavaScript. JavaScript is the world’s most widely used programming language, and its package manager is responsible for storing and distributing thousands of third-party software packages to the developer community. Yet, with greater interconnectivity comes greater vulnerability, as highlighted in 2016 when the removal of the small utility left-pad package from the npm registry caused widespread software breakage.
This research demonstrates how network measures can be used to determine the structure and complexity of the npm network and track how these parameters evolve over time. The npm network exhibits small-world behavior and a scale-free architecture, corroborating with existing studies on open-source software systems. Notably, central nodes in this network have reverse transitive dependencies numbering up to 200,000, underlining the system's vulnerability to cascading failures.

### Keywords

npm, dependency network, JavaScript, open-source, network complexity, small-world behavior, scale-free architecture

---

## 2. Small World with High Risks: A Study of Security Threats in the npm Ecosystem

### Abstract

In response to the evolving landscape of network attacks and cybersecurity, this study enhances network security by identifying critical nodes and optimizing resource allocation within budget constraints. Using node centrality scores from widely recognized centrality measures, this study proposes a unique approach to identifying network attack probabilities. By integrating predictive insights into a nonlinear optimization model, the research establishes a strategy for minimizing cyberattack risks on critical nodes and improving network robustness.
Numerical results validate the approach, improving resilience against emerging cybersecurity threats.

### Keywords

Centrality measure, Node detection, Optimization, Network security

---

## 3. Node Package Manager’s Dependency Network Robustness

### Abstract

The robustness of the npm dependency network is crucial, as many projects rely heavily on the functionality of popular packages. This paper tracks the network’s resilience over time, showing that the network is vulnerable to targeted attacks, especially on crucial nodes. Despite this, the issue is not alarming due to the strong communities supporting the packages. The study finds that the trend towards fewer dependencies and better community organization improves resilience.

### Keywords

npm, dependency network, robustness, targeted attacks, software resilience

---

## 4. On the Impact of Security Vulnerabilities in the npm Dependency Network

### Abstract

Security vulnerabilities are one of the most significant issues in open-source software libraries. This paper presents an empirical study of nearly 400 security reports over six years in the npm dependency network, analyzing the severity of vulnerabilities, their discovery and resolution, and their effects on dependent packages. The findings offer guidelines for improving security practices for package maintainers.

### Keywords

Software repository mining, Security vulnerability, Dependency network, Semantic versioning

---

## 5. Towards Using Package Centrality Trend to Identify Packages in Decline

### Abstract

Software ecosystems like npm allow code reuse but also face the challenge of identifying packages in decline. This paper proposes a scalable method using package centrality to track declining packages, providing an alternative to traditional popularity metrics. The approach accurately predicts declining packages well before current metrics show a decline.

### Keywords

Package centrality, Decline detection, Dependency graph, npm

---

## 6. Demystifying Vulnerability Propagation via Dependency Trees in npm

### Abstract

Third-party libraries with rich functionalities facilitate the fast development of JavaScript software, leading to the explosive growth of the NPM ecosystem. However, it also brings new security threats that vulnerabilities could be introduced through dependencies from third-party libraries. In particular, the threats could be excessively amplified by transitive dependencies. Existing research only considers direct dependencies or reasoning transitive dependencies based on reachability analysis, which neglects the NPM-specific dependency resolution rules as adapted during real installation, resulting in wrongly resolved dependencies. Consequently, further fine-grained analysis, such as precise vulnerability propagation and their evolution over time in dependencies, cannot be carried out precisely at a large scale, as well as deriving ecosystem-wide solutions for vulnerabilities in dependencies.
To fill this gap, we propose a knowledge graph-based dependency resolution, which resolves the inner dependency relations of dependencies as trees (i.e., dependency trees), and investigates the security threats from vulnerabilities in dependency trees at a large scale. Specifically, we first construct a complete dependency-vulnerability knowledge graph (DVGraph) that captures the whole NPM ecosystem (over 10 million library versions and 60 million well-resolved dependency relations). Based on it, we propose a novel algorithm (DTResolver) to statically and precisely resolve dependency trees, as well as transitive vulnerability propagation paths, for each package by taking the official dependency resolution rules into account. Based on that, we carry out an ecosystem-wide empirical study on vulnerability propagation and its evolution in dependency trees. Our study unveils many useful findings, and we further discuss the lessons learned and solutions for different stakeholders to mitigate the vulnerability impact in NPM based on our findings.

### Keywords

Vulnerability propagation, Dependency trees, npm, Security, Knowledge graph

---

## 7. On the Impact of Security Vulnerabilities in the npm and RubyGems Dependency Networks

### Abstract

This study compares vulnerabilities in npm and RubyGems, two major open-source ecosystems. It examines how vulnerabilities are disclosed and fixed, how they affect dependent packages, and how open-source ecosystems can improve their security practices. Findings show that npm vulnerabilities are increasing and disclosed more rapidly than RubyGems vulnerabilities.

### Keywords

Security vulnerabilities, npm, RubyGems, Package manager security

---

## 8. Towards Sustainable and Secure Reuse in Dependency Supply Chains

### Abstract

This paper explores packages at the end of the dependency chain, avoiding external dependencies and their associated risks. By analyzing npm’s most dependent packages, it argues that reducing dependencies can improve security and sustainability in software reuse.

### Keywords

Software ecosystems, Dependency supply chains, Security, Sustainable reuse

---

## 9. Structural and Connectivity Patterns in the Maven Central Software Dependency Network

### Abstract

This paper applies network science to analyze the Maven Central ecosystem, one of the largest repositories of Java libraries. By studying the connectivity and structure of this ecosystem, the paper highlights the risks posed by highly interconnected hubs and proposes strategies to mitigate these systemic risks.

### Keywords

Maven Central, Software dependencies, Dependency analysis, Network security

---

## 10. VulRG: Multi-Level Explainable Vulnerability Patch Ranking for Complex Systems Using Graphs

### Abstract

This paper introduces a novel graph-based framework for prioritizing vulnerability patches in complex systems. By integrating network communication and system dependency graphs, it provides a method for assessing risks and mitigating cyber threats, demonstrating superior accuracy in patch ranking compared to existing methods.

### Keywords

Vulnerability prioritization, Patch ranking, Cybersecurity, Graph-based framework

---

## 11. Predicting Nodal Influence via Local Iterative Metrics

### Abstract

This study investigates how combining local and global topological information can better predict a node’s influence in a network. It proposes a set of iterative metrics that incorporate progressively more global information, improving prediction accuracy in real-world and synthetic networks.

### Keywords

Nodal influence, Centrality metrics, Network prediction, Iterative metrics

---

## 12. Securing Network Resilience: Leveraging Node Centrality for Cyberattack Mitigation and Robustness Enhancement

### Abstract

This paper introduces a novel approach to enhancing network security by identifying critical nodes using centrality scores. The approach uses optimization techniques to allocate resources efficiently and minimize cyberattack risks while improving network resilience.

### Keywords

Network security, Node centrality, Cyberattack mitigation, Optimization

---
