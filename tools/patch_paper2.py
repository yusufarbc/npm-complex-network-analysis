from pathlib import Path
p = Path('paper/main.tex')
s = p.read_text(encoding='utf-8')

# 1) Insert a Parameters subsection after the Veri ve Yontem section content, before next \section{
sec_start = s.find('\\section{Veri')
if sec_start != -1:
    # Find the start of the next section after this one
    next_sec = s.find('\\section{', sec_start + 10)
    ins_point = next_sec if next_sec != -1 else sec_start + 10
    param_tex = r"""

\subsection{Parametreler}
Varsayilanlar: Top~N=200 (defterde 1000 de denenmistir), \texttt{include\_peer\_deps}=False, betweenness icin \texttt{sample\_k} \emph{otomatik} (n\leq 1200 ise tam, aksi halde k=200). Risk agirliklari: $w_{in}=0.5$, $w_{out}=0.2$, $w_b=0.3$. Ciktilar \texttt{results/} dizinine yazilir.
"""
    s = s[:ins_point] + param_tex + s[ins_point:]

# 2) Add a comprehensive outputs section before Risk Skoru Tanimi
rs_idx = s.find('\\section{Risk Skoru')
if rs_idx == -1:
    rs_idx = s.find('Risk Skoru Tan')
if rs_idx == -1:
    # Append at end if not found
    rs_idx = len(s)
outputs_tex = r"""

\section{Tum Ciktilar ve Dosya Ozeti}
\subsection{Gorseller (PNG/SVG)}
Bu calismada uretilen temel gorseller asagidadir; tamam\i results/ dizinindedir.
\begin{itemize}
  \item network\_full\_topN.(png|svg): Top N + bagimliliklarin tam agi
  \item network\_topN\_only.(png|svg): Sadece Top N ind\"uklenmis alt-ag
  \item degree\_histograms.(png|svg): In/Out-degree histogramlari (log olcek)
  \item scatter\_correlations.(png|svg): In-Degree vs Betweenness; In-Degree vs Out-Degree
  \item top10\_in\_degree.(png|svg), top10\_out\_degree.(png|svg), top10\_betweenness.(png|svg), top10\_leaders.(png|svg)
  \item top20\_risk.(png|svg): Bilesik risk skoruna gore ilk 20
  \item cascade\_impact\_top20.(png|svg): Basamaklanma etkisi (risk liderleri)
  \item risk\_vs\_cascade.(png|svg): Risk ile basamaklanma iliskisi (scatter)
\end{itemize}

\subsection{Veri ve Tablolar}
Asagidaki dosyalar metrik ve arakatman ciktilarini icerir:
\begin{longtable}{ll}
\toprule
\textbf{Dosya} & \textbf{Aciklama} \\
\midrule
\texttt{edges.csv} & Kenar listesi (source=dependent, target=dependency) \\
\texttt{metrics.csv} & Dugum metrikleri (in/out/between, is\_topN) \\
\texttt{risk\_scores.csv} & Bilesik risk skorlar\i \\
\texttt{edge\_betweenness\_top10.csv} & En yuksek edge betweenness 10 kenar \\
\texttt{robustness\_risk.json} & Risk tabanli kaldirma senaryolari icin baglanirlik \\
\texttt{graph\_stats.json} & Genel ag istatistikleri (dugum/kenar, bilesen, cap) \\
\texttt{top\_packages.txt} & Kullanilan Top N paket adlari \\
\texttt{report.md} & Kisa siralama raporu (ilk 20 listeler) \\
\texttt{metrics\_top20\_in\_degree.tex} & Top 20 In-Degree (LaTeX tablo) \\
\texttt{risk\_scores\_top20.tex} & Top 20 Risk Skoru (LaTeX tablo) \\
\texttt{cache\_deps.json} & Bagimlilik sorgulari icin onbellek \\
\bottomrule
\end{longtable}
"""
s = s[:rs_idx] + outputs_tex + s[rs_idx:]

p.write_text(s, encoding='utf-8')
print('Paper enriched with parameters and outputs summary.')
