import json
from pathlib import Path

p = Path('analysis.ipynb')
nb = json.loads(p.read_text(encoding='utf-8'))

# Helper functions

def md(cell, lines):
    cell['cell_type']='markdown'; cell['source']=lines; cell['metadata']=cell.get('metadata',{})

def replace_markdown_heading(old, new):
    for c in nb['cells']:
        if c.get('cell_type')=='markdown':
            s='\n'.join(c.get('source',[]))
            if old in s:
                c['source']=[s.replace(old,new)]

# 1) Refine intro markdown with detailed, structured explanation
intro = nb['cells'][0]
md(intro, [
    '# NPM Kompleks Ağ Analizi (Top N)',
    '',
    'Bu defter, popüler Top N NPM paketini yönlü bir ağ (Dependent → Dependency) olarak modelleyip, in-degree / out-degree / betweenness merkeziyet metrikleriyle yapısal riski inceler.',
    '',
    '**Amaç**',
    '- Bağımlılık ağındaki konuma dayalı kritik düğümleri belirlemek',
    '- Zincirleme etki (cascading impact) potansiyelini nicel görmek',
    '- Sonuçları yineleyebilir şekilde görselleştirmek ve raporlamak',
    '',
    '**Yöntem**',
    '- Veri: Liste her çalıştırmada API’lerden çekilir (ecosyste.ms / npm registry / npms.io yedekli).',
    '- Ağ Modeli: NetworkX DiGraph; kenar yönü Dependent → Dependency (bağımlı paket → bağımlılık).',
    '- Metrikler: In-Degree (gelen), Out-Degree (giden), Betweenness (köprü rol).',
    '- Performans: Büyük graf’larda betweenness yaklaşık örnekleme ile hızlandırılır.',
    '- Çıktılar: Tüm sonuçlar `results/` klasörüne kaydedilir (CSV/MD/JSON + PNG/SVG).',
    '',
    'Varsayılan Top N = 1000 (değiştirilebilir).'
])

# 2) Normalize section explanations
for i,c in enumerate(nb['cells']):
    if c.get('cell_type')=='markdown':
        s='\n'.join(c.get('source',[]))
        if s.strip().startswith('## 2) Top N Paketleri Yükle'):
            c['source']=[
                '## 2) Top N Paketleri Yükle',
                '',
                'Liste, indirilmeye göre sıralı şekilde API’lerden çekilir. Öncelik ecosyste.ms; gerekirse npm registry / npms.io yedekleri kullanılır. Bu yaklaşım sabit dosyaya bağımlılığı kaldırır ve güncel popülerliği yansıtır.'
            ]
        elif s.strip().startswith('## 3) Yönlü Ağı Kur'):
            c['source']=[
                '## 3) Yönlü Ağı Kur',
                '',
                'Kenar yönü Dependent → Dependency (paket → kullandığı bağımlılık). Bu yön, bir paketin ele geçirilmesi halinde etki akışını (bağımlıdan bağımlılığa) analiz etmeyi kolaylaştırır.'
            ]
        elif s.strip().startswith('## 4) Merkeziyet Metrikleri'):
            c['source']=[
                '## 4) Merkeziyet Metrikleri',
                '',
                '- In-Degree: Düğüme gelen kenar (bu pakete dayanan paket sayısı) → ele geçirilirse etki alanı.',
                '- Out-Degree: Düğümün dış bağımlılık sayısı → bağımlılık zinciri uzunluğu/karmaşıklığı.',
                '- Betweenness: En kısa yollardaki aracılık → köprü/tek hata noktası riski.',
                '',
                'Not: Büyük graf’larda betweenness örneklemeli (k) hesaplanır; notebook ilk hücrede `SAMPLE_K` ile ayarlanabilir.'
            ]
        elif s.strip().startswith('## 5) Liderler: İlk 10 (Özet + Görselleştirme)'):
            c['source']=[
                '## 5) Liderler: İlk 10 (Özet + Görselleştirme)',
                'In/Out-Degree ve Betweenness için ilk 10 düğümü hem metin hem grafik olarak sunar. Bu listeler ağın yapısal omurgasını ve kritik köprü düğümlerini öne çıkarır.'
            ]
        elif s.strip().startswith('## 6) Sonuçları Kaydet'):
            c['source']=[
                '## 6) Sonuçları Kaydet',
                'Kenarlıklar, merkeziyet metrikleri ve kısa rapor dosyaya yazılır. Böylece defter dışı analiz ve kıyaslamalara zemin hazırlanır.'
            ]
        elif s.strip().startswith('## 7) Hızlı Doğrulama'):
            c['source']=[
                '## 7) Hızlı Doğrulama',
                'Rastgele paketler için registry bağımlılıkları ile graf kenarlarını karşılaştırır. Küçük farklar sürüm farklılıkları ve metadata gecikmelerinden kaynaklanabilir.'
            ]
        elif s.strip().startswith('## 8) Tüm Ağ Çizimi'):
            c['source']=[
                '## 8) Tüm Ağ Çizimi (Top N + Bağımlılıklar)',
                'Top N düğümler turuncu, diğerleri mavi; düğüm boyutu in-degree ile ölçeklenir. Ağın genel topolojisi ve yıldız/omurga yapıları gözlemlenir.'
            ]
        elif s.strip().startswith('## 9) Sadece Top N'):
            c['source']=[
                '## 9) Sadece Top N (İndüklenmiş Alt-Ağ)',
                'Sadece Top N düğümlerin oluşturduğu alt-ağ; etiketler az düğüm olduğunda gösterilir. Kohort içi yapısal ilişkiler netleşir.'
            ]
        elif s.strip().startswith('## 10) Derece Dağılımları'):
            c['source']=[
                '## 10) Derece Dağılımları (Histogram)',
                'In-degree ve out-degree dağılımları (log ölçek). Kuyruk davranışı ve yoğunlaşmalar görülür.'
            ]
        elif s.strip().startswith('## 11) Korelasyonlar'):
            c['source']=[
                '## 11) Korelasyonlar (Dağılım Grafikleri)',
                'In-Degree vs Betweenness ve In-Degree vs Out-Degree ilişkileri; köprü düğümlerin derecesi ve dış bağımlılıklarının etkisi.'
            ]
        elif s.strip().startswith('## 12) Bağlanırlık ve Bileşenler'):
            c['source']=[
                '## 12) Bağlanırlık ve Bileşenler',
                'Zayıf bağlanırlık bileşen sayısı, en büyük bileşen boyutu ve ortalama dereceler. Ağın parçalanabilirliği hakkında sezgi verir.'
            ]
        elif s.strip().startswith('## 13) Köprü Kenarlar'):
            c['source']=[
                '## 13) Köprü Kenarlar (Edge Betweenness)',
                'Edge betweenness’a göre en kritik 10 kenar. Bu kenarların kopması, alt-ağların ayrışmasına yol açabilir.'
            ]
        elif s.strip().startswith('## 14) Varsayımlar ve Sınırlamalar'):
            c['source']=[
                '## 14) Varsayımlar ve Sınırlamalar',
                '- Kenar yönü Dependent → Dependency; yayılım analizi için uygundur.\n- Varsayılan olarak yalnız `dependencies` dahil; `peerDependencies` isteğe bağlı eklenebilir.\n- Global dependent sayıları dahil değildir; ecosyste.ms verisi eklenebilir.\n- En güncel sürüm kullanılır; eski sürümlerde bağımlılıklar farklı olabilir.'
            ]

# 3) Remove redundant imports in later code cells (matplotlib.pyplot repeat)
for c in nb['cells']:
    if c.get('cell_type')=='code':
        src=c.get('source',[])
        filtered=[]
        for line in src:
            if line.strip().startswith('import matplotlib.pyplot as plt'):
                # remove duplicate plt import (already in first cell)
                continue
            filtered.append(line)
        c['source']=filtered

# Save
p.write_text(json.dumps(nb, ensure_ascii=False, indent=2), encoding='utf-8')
print('OK')
