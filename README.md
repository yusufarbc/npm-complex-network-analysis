# NPM Complex Network Analysis

NPM ekosistemindeki paketleri yönlü bir ağ olarak modelleyip merkeziyet metrikleriyle yapısal riski ölçer. Amaç, klasik zafiyet skorlarının ötesine geçerek, bir paketin ağ içindeki konumundan doğan sistemik riski görünür kılmaktır.

Canlı önizleme: https://yusufarbc.github.io/npm-complex-network-analysis/

## İçindekiler
- Amaç ve Kapsam
- Proje Yapısı
- Hızlı Başlangıç
- Kullanım (Notebook ve CLI)
- Üretilen Çıktılar
- Ortam ve Sürümler
- Güvenlik Bağlamı: Eylül 2025 NPM Saldırısı

## Amaç ve Kapsam
Bu çalışma, popüler NPM paketlerinden yönlü bir bağımlılık ağı kurar; in-degree, out-degree ve betweenness merkeziyetlerini hesaplayıp min–max normalize ederek bileşik bir risk skoru üretir. Böylece, yalnızca paket içi zafiyetlere değil, bağımlılık topolojisinden kaynaklanan yapısal riske de odaklanır.

## Proje Yapısı
- `analysis/` – Notebook ve yardımcı Python kodları (veri çekme, ağ kurma, metrikler)
- `results/` – Üretilen CSV/JSON, görseller ve LaTeX tabloları
- `academic/` – LaTeX rapor kaynakları ve PDF’ler
- `.github/` – GitHub Pages dağıtım iş akışı
- `index.html` – Sonuçların statik sunumu (GitHub Pages)

Detaylar: `analysis/README.md`, `results/README.md`, `academic/README.md`.

## Hızlı Başlangıç
Önkoşul: Python 3.11.x (önerilen 3.11.9)

1) Sanal ortamı kur ve etkinleştir (Windows PowerShell)
```
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```
2) Bağımlılıkları yükle
```
pip install -r analysis/requirements.txt
```
3) Notebook’u aç (opsiyonel)
```
python -m notebook  # analysis/analysis.ipynb’i açın
```
4) Tabloları (LaTeX) üret
```
python results/make_tables.py
```
5) Sunumu görüntüle
- Yerel: `index.html`
- GitHub Pages: Actions ile otomatik dağıtım

## Kullanım
### Notebook
- `analysis/analysis.ipynb` dosyasını açın, hücreleri sırayla çalıştırın; tüm çıktılar `results/` içine yazılır.

### CLI
- Notebook olmadan üretim:
```
python -m analysis.run --topN 200 --sample-k 200
```
- Opsiyonel: `--include-peer-deps` ile `peerDependencies`’i ekleyin.

## Üretilen Çıktılar
- `results/edges.csv` – Kenar listesi (source=dependent, target=dependency)
- `results/metrics.csv` – `package,in_degree,out_degree,betweenness,is_topN`
- `results/risk_scores.csv` – Bileşik risk skoru + metrikler
- `results/graph_stats.json` – Genel ağ istatistikleri
- `results/edge_betweenness_top10.csv` – En yüksek köprü kenarlar
- `results/cascade_impact_top20.csv` – Ters yön (dependents) kaskad etkisi
- Görseller: `*.png/.svg`; Tablolar: `*.tex` (bkz. `results/make_tables.py`)

## Ortam ve Sürümler
- Python: 3.11.x (önerilen 3.11.9)
- NumPy: `>=1.23` (Python 3.11 uyumu için)
- Notebook kullanımı opsiyoneldir (`notebook`, `ipykernel`)

## Güvenlik Bağlamı: Eylül 2025 NPM Saldırısı
Kısa özet:
- Paket bakıcı hesapları phishing ile ele geçirilerek 18 popüler pakete kötü kod enjekte edildi (chalk, debug, vb.).
- Kötü kod tarayıcıda cüzdan API’lerini kancaladı, adres değiştirdi; milyarlarca indirme riske girdi.
- Olay ~2 saat içinde bastırıldı; ekosistem riski geçişli bağımlılıklardan kaynaklandı.
- Ardından “Shai‑Hulud” benzeri solucan yayılımı raporlandı; yüzlerce paketi etkiledi.

<details>
<summary>Detaylı olay akışı, tablo ve kaynaklar</summary>

Eylül 2025'te Node Package Manager (NPM) ekosistemi, tarihin en büyük tedarik zinciri saldırılarından birine maruz kaldı. Bu saldırı, phishing kampanyaları yoluyla paket bakıcılarının hesaplarının ele geçirilmesiyle başladı ve chalk, debug gibi popüler JavaScript paketlerine kötü amaçlı kod enjekte edilmesiyle devam etti. Saldırganlar, kripto para cüzdan adreslerini değiştirerek kullanıcıların fonlarını çalmayı hedefledi. Olay, açık kaynak yazılım ekosisteminin kırılganlığını bir kez daha gözler önüne serdi.

Saldırı, 5 Eylül 2025'te "npmjs.help" adlı sahte bir alan adının kaydedilmesiyle hazırlık aşamasına girdi. Bu alan, resmi NPM destek sitesini taklit ederek paket bakıcılarına phishing e-postaları gönderdi. E-postalar, iki faktörlü kimlik doğrulama (2FA) sıfırlama talebi gibi görünüyor ve bakıcıları kullanıcı adı, şifre ve TOTP kodlarını paylaşmaya ikna ediyordu. En bilinen mağdur, "qix-" olarak bilinen geliştirici Josh Junon'du. Hesabı ele geçirildikten sonra, saldırganlar 8 Eylül 2025'te saat 13:16 UTC'de kötü amaçlı sürümleri yayınlamaya başladı. Bu sürümler, tarayıcı ortamında çalışan bir "crypto-stealer" veya "wallet-drainer" içeriyordu.

Etkilenen paketler arasında chalk (konsol renklendirme), debug (hata ayıklama), ansi-styles (ANSI kodları işleme) gibi temel kütüphaneler yer alıyordu. Bu paketler, toplamda haftada 2.6 milyardan fazla indiriliyor ve birçok web uygulamasında geçişli bağımlılık olarak kullanılıyor. Saldırının mekanizması, kötü kodun tarayıcıya enjekte edilmesiyle başlıyordu: fetch, XMLHttpRequest ve cüzdan API'leri (örneğin window.ethereum, Solana API'leri) gibi işlevleri kancalıyor, ağ trafiğini izliyor ve kripto para adreslerini saldırganın kontrolündeki adreslerle değiştiriyordu. Desteklenen zincirler arasında Ethereum, Bitcoin, Solana, Tron, Litecoin ve Bitcoin Cash vardı. Kod, Levenshtein algoritması kullanarak benzer adresler üretiyor ve kullanıcı arayüzünde değişiklik yapmadan işlemi gizli tutuyordu. Ayrıca, veri hırsızlığı için hassas bilgileri exfiltre edebiliyordu.

Zaman çizelgesi şöyleydi:
- **5 Eylül 2025**: Sahte alan adı kaydedildi.
- **8 Eylül 2025, 13:16 UTC**: Kötü amaçlı sürümler yayınlandı (örneğin chalk@5.6.1, debug@4.4.2).
- **8 Eylül 2025, ~15:20 UTC**: Topluluk, GitHub'da şüpheli kodu fark etti ve uyarılar başladı.
- **8 Eylül 2025, öğleden sonra**: Bakıcılar, kötü sürümleri kaldırdı ve temiz sürümleri yayınladı. Saldırı yaklaşık 2 saat sürdü.
- **9-10 Eylül 2025**: Güvenlik firmaları (Palo Alto, Cycode) raporlar yayınladı.
- **15 Eylül 2025**: "Shai-Hulud" adlı solucan benzeri bir gelişme ortaya çıktı; bu, saldırıdan esinlenerek kendi kendine çoğalan bir malware olup yüzlerce paketi etkiledi.
- **23 Eylül 2025**: CISA, yaygın tedarik zinciri uyarısı yayınladı.

Olayın genel etkisi büyük oldu: Potansiyel olarak milyonlarca geliştirici ve milyarlarca indirme etkilendi. Kripto kayıpları sınırlı kaldı (yaklaşık 503 USD rapor edildi), çünkü erken tespit edildi. Ancak ekosistem riski yüksekti; CI/CD hatlarında çökmelere neden oldu ve web3 uygulamalarını tehdit etti. Shai-Hulud solucanı, saldırıyı genişleterek 500'den fazla paketi enfekte etti ve geliştirici kimlik bilgilerini çalmayı hedefledi.

#### Etkilenen Paketler ve Etkiler (özet tablo)

| Paket Adı | Haftalık İndirme | Rol | Saldırı Etkisi |
|---|---:|---|---|
| ansi-styles | 371.4M | ANSI stil | Tarayıcı kancaları; veri hırsızlığı |
| debug | 357.6M | Hata ayıklama | Cüzdan API’leri; işlem hijack’i |
| chalk | 299.9M | Konsol renk | Ağ izleme; adres swap’i |
| supports-color | 250M | Renk desteği | Tarayıcı entegrasyonuyla yayılım |
| strip-ansi | 200M | ANSI temizleme | Veri exfiltrasyonu |
| ... | ... | ... | ... |

#### Haber ve Rapor Kaynakları (seçme)
- Palo Alto Networks: https://www.paloaltonetworks.com/blog/cloud-security/npm-supply-chain-attack/
- CISA: https://www.cisa.gov/news-events/alerts/2025/09/23/widespread-supply-chain-compromise-impacting-npm-ecosystem
- Trend Micro: https://www.trendmicro.com/en_us/research/25/i/npm-supply-chain-attack.html
- Bleeping Computer: https://www.bleepingcomputer.com/news/security/hackers-hijack-npm-packages-with-2-billion-weekly-downloads-in-supply-chain-attack/
- Trellix: https://www.trellix.com/blogs/research/npm-account-hijacking-and-the-rise-of-supply-chain-attacks/

</details>
