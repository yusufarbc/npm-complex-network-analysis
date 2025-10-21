import json, sys
from pathlib import Path

nb_path = Path('analysis.ipynb')
nb = json.loads(nb_path.read_text(encoding='utf-8'))

md = {
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "## 11) Liderler: İlk 10 (Görselleştirme)",
        "In-degree ve betweenness için ilk 10 paketi çubuk grafiklerle gösterelim."
    ]
}

code = {
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": [
        "try:",
        "    import matplotlib.pyplot as plt",
        "    # In-Degree ilk 10 (tüm düğümler)",
        "    top10_in = sorted(in_deg.items(), key=lambda kv: kv[1], reverse=True)[:10]",
        "    names_in = [n for n,_ in top10_in][::-1]",
        "    vals_in = [v for _,v in top10_in][::-1]",
        "",
        "    # Betweenness ilk 10 (tüm düğümler)",
        "    top10_btw = sorted(btw.items(), key=lambda kv: kv[1], reverse=True)[:10]",
        "    names_btw = [n for n,_ in top10_btw][::-1]",
        "    vals_btw = [v for _,v in top10_btw][::-1]",
        "",
        "    fig, axes = plt.subplots(1, 2, figsize=(16, 6), dpi=150)",
        "    # In-Degree grafiği",
        "    axes[0].barh(names_in, vals_in, color='tab:blue')",
        "    axes[0].set_title('In-Degree İlk 10 (Tüm Düğümler)')",
        "    axes[0].set_xlabel('In-Degree')",
        "    axes[0].tick_params(axis='y', labelsize=8)",
        "",
        "    # Betweenness grafiği",
        "    axes[1].barh(names_btw, vals_btw, color='tab:orange')",
        "    axes[1].set_title('Betweenness İlk 10 (Tüm Düğümler)')",
        "    axes[1].set_xlabel('Betweenness')",
        "    axes[1].tick_params(axis='y', labelsize=8)",
        "",
        "    plt.tight_layout()",
        "    out_combo = OUTDIR / 'top10_leaders.png'",
        "    plt.savefig(out_combo)",
        "    print(out_combo)",
        "",
        "    # Ayrı ayrı da kaydedelim",
        "    plt.figure(figsize=(8,6), dpi=150)",
        "    plt.barh(names_in, vals_in, color='tab:blue')",
        "    plt.title('In-Degree İlk 10 (Tüm Düğümler)')",
        "    plt.xlabel('In-Degree')",
        "    plt.tight_layout()",
        "    out_in = OUTDIR / 'top10_in_degree.png'",
        "    plt.savefig(out_in)",
        "    print(out_in)",
        "",
        "    plt.figure(figsize=(8,6), dpi=150)",
        "    plt.barh(names_btw, vals_btw, color='tab:orange')",
        "    plt.title('Betweenness İlk 10 (Tüm Düğümler)')",
        "    plt.xlabel('Betweenness')",
        "    plt.tight_layout()",
        "    out_btw = OUTDIR / 'top10_betweenness.png'",
        "    plt.savefig(out_btw)",
        "    print(out_btw)",
        "except ModuleNotFoundError:",
        "    print('matplotlib bulunamadı; görselleştirme atlandı.')",
    ]
}

nb['cells'].append(md)
nb['cells'].append(code)

nb_path.write_text(json.dumps(nb, ensure_ascii=False, indent=2), encoding='utf-8')
print('OK')
