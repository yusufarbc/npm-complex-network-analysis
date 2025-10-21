from pathlib import Path, re
s = Path('paper/main.tex').read_text(encoding='utf-8')
# 1) Inject macro after xcolor if not present
if '\\newcommand{\\resimg}' not in s:
    s = s.replace('\\usepackage{xcolor}', '\\usepackage{xcolor}\n% Yardimci makro: results icinden gorsel ekle\n\\newcommand{\\resimg}[2][]{%\n  \\IfFileExists{../results/#2}{\\includegraphics[#1]{../results/#2}}{\\fbox{#2 bulunamadi}}%\n}')
# 2) Create mapping and simple replace for blocks
blocks = [
 ('network_full_topN.png','0.95\\linewidth'),
 ('network_topN_only.png','0.85\\linewidth'),
 ('degree_histograms.png','0.95\\linewidth'),
 ('scatter_correlations.png','0.95\\linewidth'),
 ('top10_leaders.png','0.95\\linewidth'),
 ('top10_betweenness.png','0.6\\linewidth'),
 ('top20_risk.png','0.75\\linewidth'),
 ('cascade_impact_top20.png','0.75\\linewidth'),
 ('risk_vs_cascade.png','0.6\\linewidth'),
]
for name,width in blocks:
    pat = re.compile(r"\\\\IfFileExists\{"+re.escape(name)+r"\}\{[^}]*\}\{[^}]*\}", re.DOTALL)
    s = pat.sub(r"\\resimg[width="+width+"]{"+name+r"}", s)
# pair images
s = re.sub(r"\\\\IfFileExists\{top10_in_degree\.png\}\{[^}]*\}\{[^}]*\}", r"\\resimg[width=0.48\\linewidth]{top10_in_degree.png}", s, flags=re.DOTALL)
s = re.sub(r"\\\\IfFileExists\{top10_out_degree\.png\}\{[^}]*\}\{[^}]*\}", r"\\resimg[width=0.48\\linewidth]{top10_out_degree.png}", s, flags=re.DOTALL)
Path('paper/main.tex').write_text(s, encoding='utf-8')
print('Rewrote with macro.')
