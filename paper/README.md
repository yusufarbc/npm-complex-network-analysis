Akademik Bildiri (LaTeX)
=========================

Bu klasör, çalışmanın akademik bildiri biçimindeki LaTeX dosyalarını içerir.

Derleme
-------

1) Repodaki `analysis.ipynb` defterini çalıştırarak `results/` çıktılarının üretildiğinden emin olun.
2) `paper/` klasöründe aşağıdaki komutlardan biriyle derleyin:

```
pdflatex main.tex
pdflatex main.tex  # (gerekirse ikinci kez)
```

Notlar
-----
- Görseller `../results/` altından alınır. (SVG yerine PNG tercih edilir.)
- LaTeX tabloları `results/*.tex` olarak üretilir ve `\input{...}` ile içe alınır.
- Bazı dosyalar mevcut değilse LaTeX içinde koşullu ifadeler uyarı kutusu gösterir.

