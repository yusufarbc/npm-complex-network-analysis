## analysis/ — Notebook ile calistirma (tek yol)

Bu klasordeki analiz yalnizca Jupyter Notebook uzerinden calistirilir. Lutfen `analysis/analysis.ipynb` dosyasini acip hucreleri sirayla calistirin.

Amac
- Populer NPM paketlerinden yonlu bir bagimlilik agi kurmak.
- in-degree, out-degree ve betweenness merkeziyetlerini hesaplamak.
- Min–max ile normalize edilip Bilesik Risk Skoru (BRS) uretmek.

Icerik
- `analysis.ipynb` — Adim adim veri cekme, ag kurma, metrikler ve gorsellestirme (tek calisma yolu).
- `analysis_helpers.py` — API, onbellek, metrik ve gorsellestirme yardimcilari.
- `requirements.txt` — Calisma zamani bagimliliklari.
- Kavramsal rapor ve arka plan: `academic/topolojik-risk-degerlendirmesi.md`

Kurulum
- Windows PowerShell
  - `python -m venv .venv`
  - `.\\.venv\\Scripts\\Activate.ps1`
  - `pip install -r analysis/requirements.txt`
  - `python -m pip install notebook`
- macOS/Linux
  - `python3 -m venv .venv`
  - `source .venv/bin/activate`
  - `pip install -r analysis/requirements.txt`
  - `python -m pip install notebook`

Notebook’u baslatma
- `python -m notebook` komutunu calistirin ve `analysis/analysis.ipynb` dosyasini acin.
- Hucreleri bastan sona calistirin. Varsayilan `TOP_N = 1000`, orneklemeli betweenness icin `SAMPLE_K = 200` onerilir.

Ciktilar
- Tum CSV/JSON ve gorseller `results/` dizinine yazilir.
- Onemli dosyalar: `edges.csv`, `metrics.csv`, `risk_scores.csv`, `graph_stats.json`, gorseller (PNG+SVG).

Ipucalari
- Buyuk graflarda betweenness maliyetlidir; `SAMPLE_K` kullanin.
- API kotalarinda takilirsaniz daha dusuk `TOP_N` ile tekrar deneyin ve `results/cache_deps.json` onbellegini temizleyin.
- Rastgelelik tohumlari (seed=42) ayarlidir; tekrarlanabilirlik icin koruyun.

Not
- Komut satiri CLI yurutmesi (python -m analysis.run veya python analysis/run.py) bu surumde desteklenmez.
