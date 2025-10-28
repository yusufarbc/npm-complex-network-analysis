## .github/ – GitHub Actions ve Pages

Amaç: Depoyu GitHub Pages’a statik olarak yayımlamak.

İçerik
- `workflows/static.yml` – Ana dal (`main`) pushlarında tüm repoyu Pages’a dağıtır.

Kullanım
- Manuel tetikleme: GitHub Actions → `Deploy static content to Pages` → `Run workflow`.
- Otomatik: `main` dalına push edildiğinde çalışır, `index.html` kökten servis edilir.

Notlar
- Workflow tüm depoyu yayınlar; `index.html` ve `results/` referansları olduğu gibi çalışır.
- Büyük dosyalar için LFS kullanmanız önerilir (gerekiyorsa).

