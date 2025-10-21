import re
from pathlib import Path
p = Path('paper/main.tex')
s = p.read_text(encoding='utf-8')
# Add \graphicspath if not present
if 'graphicspath' not in s:
    s = s.replace('\\usepackage{graphicx}', '\\usepackage{graphicx}\n\\graphicspath{{../results/}}')
# Replace IfFileExists blocks with direct includegraphics
s = re.sub(r"\\IfFileExists\{\.\./results/([A-Za-z0-9_\-]+\.(?:png|svg))\}\{\\includegraphics\[([^\]]*)\]\{\.\./results/\\1\}\}\{[^}]*\}", r"\\includegraphics[\2]{\1}", s)
# Also case where width only change etc (do multiple passes)
for _ in range(2):
    s = re.sub(r"\\IfFileExists\{\.\./results/([A-Za-z0-9_\-]+\.(?:png|svg))\}\{\\includegraphics\[([^\]]*)\]\{([^}]*)\}\}\{[^}]*\}", r"\\includegraphics[\2]{\1}", s)
# Save
p.write_text(s, encoding='utf-8')
print('Replaced conditionals with direct includes and set graphicspath.')
