import json
from pathlib import Path

p = Path('analysis.ipynb')
nb = json.loads(p.read_text(encoding='utf-8'))

# Fix Top10 to save SVGs
for i, cell in enumerate(nb['cells']):
    if cell.get('cell_type')=='markdown':
        src = '\n'.join(cell.get('source', []))
        if '## 11) Liderler: İlk 10' in src:
            code = nb['cells'][i+1]
            if code.get('cell_type')=='code':
                lines = code.get('source', [])
                new = []
                for line in lines:
                    new.append(line)
                    if "out_combo = OUTDIR / 'top10_leaders.png'" in line:
                        new.append("    out_combo_svg = OUTDIR / 'top10_leaders.svg'")
                    if "plt.savefig(out_combo)" in line:
                        new.append("    plt.savefig(out_combo_svg)")
                    if "plt.savefig(OUTDIR / 'top10_in_degree.png')" in line:
                        new.append("    plt.savefig(OUTDIR / 'top10_in_degree.svg')")
                    if "plt.savefig(OUTDIR / 'top10_out_degree.png')" in line:
                        new.append("    plt.savefig(OUTDIR / 'top10_out_degree.svg')")
                    if "plt.savefig(OUTDIR / 'top10_betweenness.png')" in line:
                        new.append("    plt.savefig(OUTDIR / 'top10_betweenness.svg')")
                code['source'] = new
            break

# Append new sections
cells_to_add = []

def add_md(title, desc):
    cells_to_add.append({'cell_type':'markdown','metadata':{},'source':[title, desc]})

def add_code(lines):
    cells_to_add.append({'cell_type':'code','metadata':{},'execution_count':None,'outputs':[], 'source':lines})

add_md("## 12) Derece Dağılımları (Histogram)", "In-degree ve out-degree dağılımlarını inceleyelim (log ölçek).")
add_code([
    'try:',
    '    import matplotlib.pyplot as plt',
    '    import numpy as np',
    '    indeg_vals = np.array(list(in_deg.values()))',
    '    outdeg_vals = np.array(list(out_deg.values()))',
    '    fig, ax = plt.subplots(1,2, figsize=(12,4), dpi=150)',
    "    ax[0].hist(indeg_vals, bins=30, color='tab:blue', alpha=0.8)",
    "    ax[0].set_title('In-Degree Dağılımı'); ax[0].set_yscale('log')",
    "    ax[0].set_xlabel('In-Degree'); ax[0].set_ylabel('Frekans')",
    "    ax[1].hist(outdeg_vals, bins=30, color='tab:green', alpha=0.8)",
    "    ax[1].set_title('Out-Degree Dağılımı'); ax[1].set_yscale('log')",
    "    ax[1].set_xlabel('Out-Degree'); ax[1].set_ylabel('Frekans')",
    '    plt.tight_layout()',
    "    plt.savefig(OUTDIR / 'degree_histograms.png')",
    "    plt.savefig(OUTDIR / 'degree_histograms.svg')",
    'except ModuleNotFoundError:',
    "    print('matplotlib bulunamadı; görselleştirme atlandı.')",
])

add_md("## 13) Korelasyonlar (Dağılım Grafikleri)", "In-degree vs Betweenness ve In-degree vs Out-degree.")
add_code([
    'try:',
    '    import matplotlib.pyplot as plt',
    '    import numpy as np',
    '    nodes_list = list(G.nodes())',
    '    x_in = np.array([in_deg.get(n,0) for n in nodes_list])',
    '    y_btw = np.array([btw.get(n,0.0) for n in nodes_list])',
    '    y_out = np.array([out_deg.get(n,0) for n in nodes_list])',
    '    fig, ax = plt.subplots(1,2, figsize=(12,4), dpi=150)',
    "    ax[0].scatter(x_in, y_btw, s=10, alpha=0.6, color='tab:orange')",
    "    ax[0].set_title('In-Degree vs Betweenness')",
    "    ax[0].set_xlabel('In-Degree'); ax[0].set_ylabel('Betweenness')",
    "    ax[1].scatter(x_in, y_out, s=10, alpha=0.6, color='tab:green')",
    "    ax[1].set_title('In-Degree vs Out-Degree')",
    "    ax[1].set_xlabel('In-Degree'); ax[1].set_ylabel('Out-Degree')",
    '    plt.tight_layout()',
    "    plt.savefig(OUTDIR / 'scatter_correlations.png')",
    "    plt.savefig(OUTDIR / 'scatter_correlations.svg')",
    'except ModuleNotFoundError:',
    "    print('matplotlib bulunamadı; görselleştirme atlandı.')",
])

add_md("## 14) Bağlanırlık ve Bileşenler", "Zayıf bağlanırlık bileşenleri ve temel ağ istatistikleri.")
add_code([
    'import json',
    'import networkx as nx',
    'W = G.to_undirected()',
    'components = list(nx.connected_components(W))',
    'components_sizes = sorted([len(c) for c in components], reverse=True)',
    'stats = {',
    "    'nodes': G.number_of_nodes(),",
    "    'edges': G.number_of_edges(),",
    "    'components_count': len(components),",
    "    'largest_component_size': components_sizes[0] if components_sizes else 0,",
    "    'avg_in_degree': (sum(in_deg.values())/len(in_deg)) if in_deg else 0,",
    "    'avg_out_degree': (sum(out_deg.values())/len(out_deg)) if out_deg else 0,",
    '}',
    "(OUTDIR / 'graph_stats.json').write_text(json.dumps(stats, ensure_ascii=False, indent=2), encoding='utf-8')",
    'stats'
])

add_md("## 15) Köprü Kenarlar (Edge Betweenness)", "En yüksek edge betweenness değerine sahip 10 kenarı çıkaralım.")
add_code([
    'import csv',
    'import networkx as nx',
    'eb = nx.edge_betweenness_centrality(G, normalized=True)',
    'top_edges = sorted(eb.items(), key=lambda kv: kv[1], reverse=True)[:10]',
    "with (OUTDIR / 'edge_betweenness_top10.csv').open('w', newline='', encoding='utf-8') as f:",
    "    w = csv.writer(f); w.writerow(['u','v','edge_betweenness'])",
    "    [w.writerow([u,v, f'{val:.6f}']) for (u,v), val in top_edges]",
    'top_edges'
])

nb['cells'].extend(cells_to_add)

p.write_text(json.dumps(nb, ensure_ascii=False, indent=2), encoding='utf-8')
print('OK')
