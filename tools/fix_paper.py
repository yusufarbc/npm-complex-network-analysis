from pathlib import Path, re
p = Path('paper/main.tex')
s = p.read_text(encoding='utf-8')
# Fix Parametreler math
s = s.replace("(n\\leq 1200 ise tam, aksi halde k=200)", "($n\\leq 1200$ ise tam, aksi halde $k=200$)")
# Fix broken accent macro sequence in cascading paragraph
s = s.replace('dok\\"ulm\\u\\c{s}t\\u{u}r.', 'dokulmustur.')
# Also guard if other accented leftovers exist
s = s.replace('d\\"ok\\"ul', 'dokul')
Path('paper/main.tex').write_text(s, encoding='utf-8')
print('Paper fixes applied.')
