from pathlib import Path
p = Path('paper/main.tex')
s = p.read_text(encoding='utf-8')

# Insert after first \end{itemize}
idx = s.find('\\end{itemize}')
if idx != -1:
    insert_point = idx + len('\\end{itemize}')
    amac = r"""

\section{\c{C}al\i\c{s}man\i n Amac\i}
Bu \c{c}al\i\c{s}man\i n temel amac\i, yaz\i l\i m tedarik zinciri g\"uvenli\u{g}ini yap\i sal bir bak\i\c{s} a\c{c}\i s\i yla yeniden tan\i mlamak ve mevcut g\"uvenlik de\u{g}erlendirme yakla\c{s}\i mlar\i na a\u{g} bilimi temelli bir \"o\l c\"ut kazand\i rmakt\i r. Geleneksel sistemler (\"or. CVSS), riski yaln\i zca paket i\c{c}i zafiyetlerle \"ol\c{c}erken; ger\c{c}ekte risk, paketin ba\u{g}\i ml\i oldu\u{g}u ve kendisine ba\u{g}\i ml\i olan paketlerle kurdu\u{g}u ili\c{s}kilerden de kaynaklan\i r. Bu nedenle NPM ekosistemindeki paketleri bir \emph{karma\c{s}\i k a\u{g}} olarak modelleyerek, her bir paketin a\u{g} i\c{c}indeki yap\i sal \"onemini, ele ge\c{c}irilmesi durumunda yaratabilece\u{g}i basamaklanma (\emph{cascading}) etkisini ve bunun sistemik g\"uvenlik riski \"uzerindeki nicel etkilerini bilimsel metriklerle \"ol\c{c}meyi ve \"ong\"ormeyi hedefliyoruz.
"""
    s = s[:insert_point] + amac + s[insert_point:]

# Insert cascading impact after risk_scores_top20.tex line
marker = '../results/risk_scores_top20.tex'
pos = s.find(marker)
if pos != -1:
    line_end = s.find('\n', pos)
    if line_end == -1:
        line_end = len(s)
    extra = r"""

\subsection{Basamaklanma (Cascading Impact)}
Bir d\"u\u{g}\u m\"un ele ge\c{c}irilmesi halinde, ters y\"onde (dependents) ula\c{s}\i labilen d\"u\u{g}\u m say\i s\i o d\"u\u{g}\u m\"un potansiyel etki alan\i n\i g\"osterir. Risk liderleri i\c{c}in hesaplanan basamaklanma etkisi a\c{s}a\u{g}\i daki g\"orsele d\"ok\"ulm\u\c{s}t\u{u}r.
\begin{figure}[h]
  \centering
  \IfFileExists{cascade_impact_top20.png}{\includegraphics[width=0.75\linewidth]{../results/cascade_impact_top20.png}}{\fbox{cascade\_impact\_top20.png bulunamad\i}}
  \caption{Risk skoruna g\"ore ilk 20 paket i\c{c}in basamaklanma (cascading impact) b\"uy\"ukl\"u\u{g}\u{u}.}
\end{figure}

\paragraph{Risk--Basamaklanma \c{C}izimi.} Ek olarak, risk skoru ile basamaklanma etkisi aras\i ndaki ili\c{s}ki de g\"ozlemlenmi\c{s}tir.
\begin{figure}[h]
  \centering
  \IfFileExists{risk_vs_cascade.png}{\includegraphics[width=0.6\linewidth]{../results/risk_vs_cascade.png}}{\fbox{risk\_vs\_cascade.png bulunamad\i}}
  \caption{Risk skoru ile basamaklanma etkisi aras\i ndaki ili\c{s}ki (scatter).}
\end{figure}
"""
    s = s[:line_end] + extra + s[line_end:]

p.write_text(s, encoding='utf-8')
print('Paper patched.')
