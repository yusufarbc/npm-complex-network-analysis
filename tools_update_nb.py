import json
from pathlib import Path

p = Path('analysis.ipynb')
nb = json.loads(p.read_text(encoding='utf-8'))

# 1) Update compute_metrics assignment to include out_deg
for cell in nb['cells']:
    if cell.get('cell_type')=='code':
        src = '\n'.join(cell.get('source', []))
        if 'in_deg, btw = compute_metrics(G)' in src:
            cell['source'] = [s.replace('in_deg, btw = compute_metrics(G)', 'in_deg, out_deg, btw = compute_metrics(G)') for s in cell['source']]
        if 'save_metrics(in_deg, btw, top_set' in src:
            cell['source'] = [s.replace('save_metrics(in_deg, btw, top_set', 'save_metrics(in_deg, out_deg, btw, top_set') for s in cell['source']]
        if 'save_report(in_deg, btw, top_set' in src:
            cell['source'] = [s.replace('save_report(in_deg, btw, top_set', 'save_report(in_deg, out_deg, btw, top_set') for s in cell['source']]

# 2) Update centrality markdown to mention out-degree
for cell in nb['cells']:
    if cell.get('cell_type')=='markdown':
        text = '\n'.join(cell.get('source', []))
        if '## 4) Merkeziyet Metrikleri' in text and 'Out-Degree' not in text:
            cell['source'] = [
                '## 4) Merkeziyet Metrikleri\n',
                '- In-Degree: Düğüme gelen kenar → etkilenebilecek alan\n',
                '- Out-Degree: Düğümün dış bağımlılık sayısı → bağımlılık zinciri uzunluğu\n',
                '- Betweenness: En kısa yollardaki aracılık → tek hata noktası riski'
            ]

# 3) Extend Top10 visualization to include out-degree
for i, cell in enumerate(nb['cells']):
    if cell.get('cell_type')=='markdown':
        s='\n'.join(cell.get('source', []))
        if '## 11) Liderler: İlk 10' in s:
            # Next code cell should be bar charts; modify to 3-panel
            code = nb['cells'][i+1]
            code['source'] = [
                'try:',
                '    import matplotlib.pyplot as plt',
                '    # In-Degree ilk 10 (tüm düğümler)',
                '    top10_in = sorted(in_deg.items(), key=lambda kv: kv[1], reverse=True)[:10]',
                '    names_in = [n for n,_ in top10_in][::-1]',
                '    vals_in = [v for _,v in top10_in][::-1]',
                '',
                '    # Out-Degree ilk 10 (tüm düğümler)',
                '    top10_out = sorted(out_deg.items(), key=lambda kv: kv[1], reverse=True)[:10]',
                '    names_out = [n for n,_ in top10_out][::-1]',
                '    vals_out = [v for _,v in top10_out][::-1]',
                '',
                '    # Betweenness ilk 10 (tüm düğümler)',
                '    top10_btw = sorted(btw.items(), key=lambda kv: kv[1], reverse=True)[:10]',
                '    names_btw = [n for n,_ in top10_btw][::-1]',
                '    vals_btw = [v for _,v in top10_btw][::-1]',
                '',
                '    fig, axes = plt.subplots(1, 3, figsize=(20, 6), dpi=150)',
                '    # In-Degree grafiği',
                "    axes[0].barh(names_in, vals_in, color='tab:blue')",
                "    axes[0].set_title('In-Degree İlk 10')",
                "    axes[0].set_xlabel('In-Degree')",
                "    axes[0].tick_params(axis='y', labelsize=8)",
                '',
                '    # Out-Degree grafiği',
                "    axes[1].barh(names_out, vals_out, color='tab:green')",
                "    axes[1].set_title('Out-Degree İlk 10')",
                "    axes[1].set_xlabel('Out-Degree')",
                "    axes[1].tick_params(axis='y', labelsize=8)",
                '',
                '    # Betweenness grafiği',
                "    axes[2].barh(names_btw, vals_btw, color='tab:orange')",
                "    axes[2].set_title('Betweenness İlk 10')",
                "    axes[2].set_xlabel('Betweenness')",
                "    axes[2].tick_params(axis='y', labelsize=8)",
                '',
                '    plt.tight_layout()',
                "    out_combo = OUTDIR / 'top10_leaders.png'",
                '    plt.savefig(out_combo)',
                '    print(out_combo)',
                '',
                '    # Ayrı ayrı da kaydedelim',
                "    plt.figure(figsize=(8,6), dpi=150); plt.barh(names_in, vals_in, color='tab:blue'); plt.title('In-Degree İlk 10'); plt.xlabel('In-Degree'); plt.tight_layout(); plt.savefig(OUTDIR / 'top10_in_degree.png')",
                "    plt.figure(figsize=(8,6), dpi=150); plt.barh(names_out, vals_out, color='tab:green'); plt.title('Out-Degree İlk 10'); plt.xlabel('Out-Degree'); plt.tight_layout(); plt.savefig(OUTDIR / 'top10_out_degree.png')",
                "    plt.figure(figsize=(8,6), dpi=150); plt.barh(names_btw, vals_btw, color='tab:orange'); plt.title('Betweenness İlk 10'); plt.xlabel('Betweenness'); plt.tight_layout(); plt.savefig(OUTDIR / 'top10_betweenness.png')",
                'except ModuleNotFoundError:',
                "    print('matplotlib bulunamadı; görselleştirme atlandı.')",
            ]
            break

p.write_text(json.dumps(nb, ensure_ascii=False, indent=2), encoding='utf-8')
print('OK')
