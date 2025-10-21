from pathlib import Path, re
p = Path('paper/main.tex')
s = p.read_text(encoding='utf-8')
# Replace the problematic sentence in cascading impact subsection with ASCII-safe text
s = re.sub(r"Bir d.*?g\\\"orsele.*?\.",
           r"Risk liderleri icin hesaplanan basamaklanma etkisi asagidaki gorselde sunulmustur.",
           s, flags=re.DOTALL)
Path('paper/main.tex').write_text(s, encoding='utf-8')
print('Replaced problematic cascading sentence.')
