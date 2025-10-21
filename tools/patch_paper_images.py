import re
from pathlib import Path
p = Path('paper/main.tex')
s = p.read_text(encoding='utf-8')
# Remove our wrapper macro if present
s = re.sub(r"\n\\let\\OrigIfFileExists\\IfFileExists\s*\n\\renewcommand\{\\IfFileExists\}\[3\]\{[^}]*\}\s*\n","\n", s, flags=re.DOTALL)
# Replace all tests to point to ../results/<file>
s = re.sub(r"\\IfFileExists\{(?!\.\./results/)([A-Za-z0-9_\-]+\.(?:png|svg))\}", r"\\IfFileExists{../results/\1}", s)
# Save back
p.write_text(s, encoding='utf-8')
print('Patched main.tex: removed wrapper and updated image tests to ../results/.')
