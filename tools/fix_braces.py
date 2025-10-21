from pathlib import Path, re
p = Path('paper/main.tex')
s = p.read_text(encoding='utf-8')
# Collapse any includegraphics line ending with double closing braces -> single
s = re.sub(r"(\\includegraphics\[[^\]]*\]\{[^}]*\})\}\s*$", r"\1\n", s, flags=re.MULTILINE)
# Also safely remove stray '}' immediately following includegraphics
s = re.sub(r"(\\includegraphics\[[^\]]*\]\{[^}]*\})\}\s*", r"\1\n", s)
Path('paper/main.tex').write_text(s, encoding='utf-8')
print('Fixed stray braces after includegraphics.')
