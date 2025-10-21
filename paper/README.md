Akademik Bildiri (LaTeX)
=========================

Bu klasör, çalışmanın akademik bildiri biçimindeki LaTeX dosyalarını içerir.

Derleme
-------

1) Repodaki analysis.ipynb defterini çalıştırarak `results/` çıktılarının üretildiğinden emin olun.
2) `paper/` klasöründe aşağıdaki komutlardan biriyle derleyin:

```
pdflatex main.tex
pdflatex main.tex  # (gerekirse ikinci kez)
```

Notlar
-----
- Görseller `../results/` altından alınır. PNG var ise doğrudan eklenir. (SVG yerine PNG kullanılır.)
- CSV tabloları için `csvsimple` paketi kullanılmıştır; `edge_betweenness_top10.csv` tablo olarak içe aktarılır.
- Eğer bazı dosyalar mevcut değilse, LaTeX içinde koşullu ifadeler uyarı kutusu gösterir.

