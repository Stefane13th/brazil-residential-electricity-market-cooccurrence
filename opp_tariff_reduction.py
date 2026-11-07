import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import FancyBboxPatch, Circle
import os

# ============================================================
# 1. DADOS
# ============================================================

regions = [
    "Southeast",
    "South",
    "Central-West",
    "Northeast",
    "North"
]

regional_total = np.array([17, 16, 5, 2, 0])
regional_mentions = np.array([10, 9, 2, 1, 0])
regional_no_mentions = np.array([7, 7, 3, 1, 0])

profiles = [
    "Installation",
    "Consultancy",
    "Search",
    "Government",
    "Association",
    "Utility Company",
    "Does not address\nthe topic"
]

profile_counts = np.array([9, 6, 3, 2, 1, 1, 18])
profile_percentages = profile_counts / 40 * 100

heatmap_profiles = [
    "Association",
    "Government",
    "Consultancy",
    "Installation",
    "Search",
    "Utility Company"
]

heatmap_regions = [
    "Southeast",
    "South",
    "Central-West",
    "Northeast",
    "North"
]

heatmap_data = np.array([
    [0, 0, 1, 0, 0],  # Association
    [1, 1, 0, 0, 0],  # Government
    [2, 1, 3, 0, 0],  # Consultancy
    [5, 4, 0, 0, 0],  # Installation
    [1, 2, 0, 0, 0],  # Search
    [1, 0, 0, 0, 0]   # Utility Company
])

participants = [
    ("Association", "Central-West", "AS2"),
    ("Government", "Southeast", "CA1"),
    ("Government", "Central-West", "CA2"),
    ("Consultancy", "South", "CT1, CT2, CT7"),
    ("Consultancy", "Southeast", "CT5, CT6"),
    ("Consultancy", "Northeast", "CT8"),
    ("Installation", "Southeast",
     "CP2, CP8, CP11, CP13, CP14"),
    ("Installation", "South",
     "CP6, CP9, CP12, CP16"),
    ("Search", "Southeast", "R3"),
    ("Search", "South", "R4, R5"),
    ("Utility Company", "Southeast", "U4")
]

# ============================================================
# 2. ESTILO VISUAL
# ============================================================

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 14,
    "axes.titlesize": 16,
    "axes.labelsize": 14,
    "xtick.labelsize": 14,
    "ytick.labelsize": 14,
    "figure.facecolor": "white",
    "axes.facecolor": "white",
    "savefig.facecolor": "white"
})

navy = "#17457A"
blue = "#2878B5"
teal = "#078F8A"
orange = "#F28B45"
grey = "#A4AFBA"
light_blue = "#EAF3FA"
grid_color = "#D8E2EC"

# ============================================================
# 3. CRIAR FIGURA COM TRÊS PAINÉIS
# ============================================================

# Aumentei a altura total da figura para acomodar as tabelas maiores
fig = plt.figure(figsize=(22, 16), constrained_layout=False)

gs = fig.add_gridspec(
    nrows=2,
    ncols=3,
    height_ratios=[2.2, 1.4],  # Mais espaço vertical para o painel inferior
    width_ratios=[1.05, 1.05, 1.0],
    left=0.045,
    right=0.975,
    top=0.90,
    bottom=0.08,  # Mais espaço para a nota metodológica
    wspace=0.38,
    hspace=0.50   # Mais separação entre gráficos e tabelas
)

ax_a = fig.add_subplot(gs[0, 0])
ax_b = fig.add_subplot(gs[0, 1])
ax_c = fig.add_subplot(gs[0, 2])
ax_table = fig.add_subplot(gs[1, :])

# Título geral
fig.suptitle(
    "Geographical and Professional Distribution of the "
    "Tariff Reduction Opportunity Among Specialists",
    fontsize=22,
    fontweight="bold",
    color="white",
    x=0.5,
    y=0.975,
    bbox=dict(
        boxstyle="round,pad=0.65",
        facecolor=navy,
        edgecolor=navy
    )
)

# ============================================================
# 4. PAINEL A — DISTRIBUIÇÃO REGIONAL
# ============================================================

y = np.arange(len(regions))

ax_a.barh(
    y,
    regional_mentions,
    color=teal,
    label="Addresses tariff reduction",
    height=0.75
)

ax_a.barh(
    y,
    regional_no_mentions,
    left=regional_mentions,
    color=orange,
    label="Does not address tariff reduction",
    height=0.75
)

for i, (yes, no, total) in enumerate(
    zip(regional_mentions, regional_no_mentions, regional_total)
):
    if total > 0:
        pct_yes = yes / total * 100
        pct_no = no / total * 100

        if yes >= 2:
            ax_a.text(
                yes / 2, i,
                f"{yes}\n({pct_yes:.0f}%)",
                ha="center", va="center",
                color="white", fontweight="bold",
                fontsize=13
            )
        else:
            ax_a.text(
                yes / 2, i,
                str(yes),
                ha="center", va="center",
                color="white", fontweight="bold",
                fontsize=13
            )

        if no >= 2:
            ax_a.text(
                yes + no / 2, i,
                f"{no}\n({pct_no:.0f}%)",
                ha="center", va="center",
                color="white", fontweight="bold",
                fontsize=13
            )
        else:
            ax_a.text(
                yes + no / 2, i,
                str(no),
                ha="center", va="center",
                color="white", fontweight="bold",
                fontsize=13
            )

        ax_a.text(
            total + 0.45, i,
            str(total),
            va="center",
            color=navy,
            fontweight="bold",
            fontsize=14
        )
    else:
        ax_a.text(
            3.0, i, "No respondents",
            ha="center", va="center",
            color=navy,
            fontsize=12
        )

ax_a.set_yticks(y)
ax_a.set_yticklabels([
    f"{r}\n(n = {n})"
    for r, n in zip(regions, regional_total)
])
ax_a.invert_yaxis()
ax_a.set_xlim(0, 21)
ax_a.set_xlabel("Number of specialists", fontsize=14)
ax_a.set_title(
    "(a) Regional distribution",
    loc="left", color=navy, fontweight="bold", pad=12
)

ax_a.grid(axis="x", color=grid_color, alpha=0.7)
ax_a.set_axisbelow(True)

ax_a.legend(
    loc="lower center",
    bbox_to_anchor=(0.5, -0.22),
    frameon=False,
    fontsize=13,
    ncol=2
)

# ============================================================
# 5. PAINEL B — PERFIS PROFISSIONAIS
# ============================================================

y_b = np.arange(len(profiles))

colors_b = [
    blue, blue, blue, blue, blue, blue, grey
]

bars = ax_b.barh(
    y_b,
    profile_counts,
    color=colors_b,
    height=0.75
)

for bar, count, pct in zip(
    bars, profile_counts, profile_percentages
):
    ax_b.text(
        count + 0.4,
        bar.get_y() + bar.get_height() / 2,
        f"{count} ({pct:.1f}%)",
        va="center",
        color=navy,
        fontweight="bold",
        fontsize=13
    )

ax_b.set_yticks(y_b)
ax_b.set_yticklabels([
    f"{p}\n(n = {n})"
    for p, n in zip(profiles, profile_counts)
])
ax_b.invert_yaxis()
ax_b.set_xlim(0, 23)
ax_b.set_xlabel("Number of specialists", fontsize=14)
ax_b.set_title(
    "(b) Professional profile distribution",
    loc="left", color=navy, fontweight="bold", pad=12
)
ax_b.grid(axis="x", color=grid_color, alpha=0.7)
ax_b.set_axisbelow(True)

# ============================================================
# 6. PAINEL C — HEATMAP PERFIL X REGIÃO
# ============================================================

cmap = LinearSegmentedColormap.from_list(
    "custom_blue",
    ["#EDF5FC", "#7BB5E2", "#1764AD"]
)

im = ax_c.imshow(
    heatmap_data,
    cmap=cmap,
    aspect="auto",
    vmin=0,
    vmax=5
)

ax_c.set_xticks(np.arange(len(heatmap_regions)))
ax_c.set_xticklabels(
    heatmap_regions,
    rotation=35,
    ha="right",
    fontsize=13
)
ax_c.set_yticks(np.arange(len(heatmap_profiles)))
ax_c.set_yticklabels(heatmap_profiles, fontsize=13)

ax_c.set_title(
    "(c) Professional profile by region",
    loc="left", color=navy, fontweight="bold", pad=12
)

for i in range(heatmap_data.shape[0]):
    for j in range(heatmap_data.shape[1]):
        value = heatmap_data[i, j]
        ax_c.text(
            j, i, str(value),
            ha="center", va="center",
            color="white" if value >= 3 else navy,
            fontweight="bold" if value > 0 else "normal",
            fontsize=15
        )

ax_c.set_xticks(
    np.arange(-0.5, len(heatmap_regions), 1),
    minor=True
)
ax_c.set_yticks(
    np.arange(-0.5, len(heatmap_profiles), 1),
    minor=True
)
ax_c.grid(which="minor", color="white", linewidth=1.5)
ax_c.tick_params(which="minor", bottom=False, left=False)

cbar = fig.colorbar(
    im,
    ax=ax_c,
    fraction=0.046,
    pad=0.04
)
cbar.set_label("Number of specialists", fontsize=13)

# ============================================================
# 7. PAINEL INFERIOR — IDENTIFICADORES DOS PARTICIPANTES
# ============================================================

ax_table.axis("off")

# Título do painel inferior
ax_table.text(
    0.01, 1.10,
    "Sample summary and participant traceability — Specialists who address the Tariff Reduction Opportunity (n=22)",
    fontsize=22,
    color=navy,
    fontweight="bold",
    va="top",
    transform=ax_table.transAxes
)

# Caixas de resumo — reposicionadas para não sobrepor as tabelas
ax_table.text(
    0.01, 0.82,
    "TOTAL SAMPLE\n40 specialists",
    fontsize=14,
    color=navy,
    fontweight="bold",
    va="top",
    transform=ax_table.transAxes,
    bbox=dict(
        boxstyle="round,pad=0.6",
        facecolor=light_blue,
        edgecolor="#B8D6EC"
    )
)

ax_table.text(
    0.01, 0.52,
    "MENTION TARIFF REDUCTION\n22 specialists (55%)",
    fontsize=14,
    color=teal,
    fontweight="bold",
    va="top",
    transform=ax_table.transAxes,
    bbox=dict(
        boxstyle="round,pad=0.6",
        facecolor="#E7F5F4",
        edgecolor="#A9DCD8"
    )
)

df = pd.DataFrame(
    participants,
    columns=["Profile", "Region", "Participants (IDs)"]
)

df_left = df.iloc[:6]
df_right = df.iloc[6:]

def draw_table(ax, dataframe, bbox):
    table = ax.table(
        cellText=dataframe.values,
        colLabels=dataframe.columns,
        cellLoc="left",
        colLoc="left",
        bbox=bbox,
        colWidths=[0.24, 0.26, 0.50]
    )

    table.auto_set_font_size(False)
    table.set_fontsize(16)

    for (row, col), cell in table.get_celld().items():
        cell.set_edgecolor("#B8D6EC")
        cell.set_linewidth(0.7)
        cell.set_height(cell.get_height() * 1.15)  # Células mais altas

        if row == 0:
            cell.set_facecolor("#DCEAF5")
            cell.set_text_props(
                color=navy,
                weight="bold",
                fontsize=16
            )
        else:
            cell.set_facecolor(
                "white" if row % 2 else "#F5F9FC"
            )
            cell.set_text_props(
                color=navy,
                fontsize=16
            )

    return table

# Ajustei os bboxes: mais altura (0.82) e largura proporcional
# Tabela esquerda: começa em x=0.28, largura 0.34
draw_table(
    ax_table,
    df_left,
    bbox=[0.28, 0.08, 0.34, 0.82]
)

# Tabela direita: começa em x=0.65, largura 0.34
draw_table(
    ax_table,
    df_right,
    bbox=[0.65, 0.08, 0.34, 0.82]
)

# Nota metodológica
fig.text(
    0.045, 0.015,
    "Note: Percentages are calculated relative to the full sample (n = 40). "
    "Unverified profile-region combinations should not be interpreted as confirmed zeros.",
    fontsize=20,
    color="#526579"
)

# ============================================================
# 8. SALVAR E EXIBIR
# ============================================================

script_dir = os.path.dirname(os.path.abspath(__file__))
path_png = os.path.join(script_dir, "tariff_reduction_three_panels.png")
path_pdf = os.path.join(script_dir, "tariff_reduction_three_panels.pdf")

plt.savefig(
    path_png,
    dpi=300,
    bbox_inches="tight"
)

plt.savefig(
    path_pdf,
    bbox_inches="tight"
)

plt.show()

print("Files saved:")
print(f"- {path_png}")