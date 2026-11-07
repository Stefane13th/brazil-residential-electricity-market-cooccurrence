import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import os

# ============================================================
# 1. DADOS — Melhoria: Clear Rules (Regras Claras)
# ============================================================

regions = [
    "Southeast",
    "South",
    "Central-West",
    "Northeast",
    "North"
]

# Dados da Tabela 1: Região x Especialistas
regional_total = np.array([17, 16, 5, 2, 0])
regional_mentions = np.array([5, 4, 3, 2, 0])       # Tratam a melhoria
regional_no_mentions = np.array([12, 12, 2, 0, 0])  # Não tratam a melhoria

# Dados da Tabela 2: Perfil x Imp_ClearRules
profiles = [
    "Association",
    "Consultancy",
    "Installation",
    "Search",
    "Utility Company",
    "Does not address\nthe topic"
]

profile_counts = np.array([1, 4, 2, 4, 3, 26])
profile_percentages = profile_counts / 40 * 100

# Heatmap: Perfil x Região (distribuição dos 14 que mencionam)
heatmap_profiles = [
    "Association",
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

# Distribuição dos 14 especialistas que mencionam a melhoria
# Association: Central-West=1
# Consultancy: Southeast=1, Central-West=1, South=1, Northeast=1
# Installation: Southeast=1, South=1
# Search: Southeast=2, South=2
# Utility Company: Southeast=1, Central-West=1, Northeast=1
heatmap_data = np.array([
    [0, 0, 1, 0, 0],  # Association (1)
    [1, 1, 1, 1, 0],  # Consultancy (4)
    [1, 1, 0, 0, 0],  # Installation (2)
    [2, 2, 0, 0, 0],  # Search (4)
    [1, 0, 1, 1, 0]   # Utility Company (3)
])

# Lista de participantes que MENCIONAM a melhoria (14 especialistas)
participants = [
    ("Association", "Central-West", "AS3"),
    ("Consultancy", "Southeast", "CT3"),
    ("Consultancy", "Central-West", "CT4"),
    ("Consultancy", "South", "CT7"),
    ("Consultancy", "Northeast", "CT8"),
    ("Installation", "Southeast", "CP14"),
    ("Installation", "South", "CP12"),
    ("Search", "Southeast", "R3, R4"),
    ("Search", "South", "R5, R6"),
    ("Utility Company", "Southeast", "U4"),
    ("Utility Company", "Central-West", "U2"),
    ("Utility Company", "Northeast", "U3")
]

# ============================================================
# 2. ESTILO VISUAL
# ============================================================

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 16,
    "axes.titlesize": 18,
    "axes.labelsize": 16,
    "xtick.labelsize": 16,
    "ytick.labelsize": 16,
    "figure.facecolor": "white",
    "axes.facecolor": "white",
    "savefig.facecolor": "white"
})

# Paleta de cores — AZUL para melhoria
navy = "#17457A"
blue_improvement = "#1f77b4"    # Azul: aborda a melhoria
grey_light = "#cccccc"          # Cinza: não aborda
blue_profile = "#2878B5"        # Azul: perfis
grey_profile = "#A4AFBA"        # Cinza: não aborda
light_blue_imp = "#E6F0FA"      # Fundo azul claro para caixa de resumo
light_blue_box = "#EAF3FA"      # Fundo azul claro para "Total Sample"
grid_color = "#D8E2EC"

# ============================================================
# 3. CRIAR FIGURA COM TRÊS PAINÉIS
# ============================================================

fig = plt.figure(figsize=(24, 18), constrained_layout=False)

gs = fig.add_gridspec(
    nrows=2,
    ncols=3,
    height_ratios=[2.2, 1.4],
    width_ratios=[1.05, 1.05, 1.0],
    left=0.045,
    right=0.975,
    top=0.90,
    bottom=0.08,
    wspace=0.38,
    hspace=0.50
)

ax_a = fig.add_subplot(gs[0, 0])
ax_b = fig.add_subplot(gs[0, 1])
ax_c = fig.add_subplot(gs[0, 2])
ax_table = fig.add_subplot(gs[1, :])

# Título geral
fig.suptitle(
    "Geographical and Professional Distribution of the "
    "Clear Rules Improvement Among Specialists",
    fontsize=24,
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
    color=blue_improvement,
    label="Addresses the improvement",
    height=0.75
)

ax_a.barh(
    y,
    regional_no_mentions,
    left=regional_mentions,
    color=grey_light,
    label="Does not address the improvement",
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
            fontsize=14
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
    blue_profile, blue_profile, blue_profile, blue_profile, blue_profile, grey_profile
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
        fontsize=15
    )

ax_b.set_yticks(y_b)
ax_b.set_yticklabels([
    f"{p}\n(n = {n})"
    for p, n in zip(profiles, profile_counts)
])
ax_b.invert_yaxis()
ax_b.set_xlim(0, 35)
ax_b.set_xlabel("Number of specialists", fontsize=16)
ax_b.set_title(
    "(b) Professional profile distribution",
    loc="left", color=navy, fontweight="bold", pad=12, fontsize=18
)
ax_b.grid(axis="x", color=grid_color, alpha=0.7)
ax_b.set_axisbelow(True)

# ============================================================
# 6. PAINEL C — HEATMAP PERFIL X REGIÃO
# ============================================================

# Colormap azul para a melhoria
cmap = LinearSegmentedColormap.from_list(
    "custom_blue",
    ["#EDF5FC", "#7BB5E2", "#1f77b4"]
)

im = ax_c.imshow(
    heatmap_data,
    cmap=cmap,
    aspect="auto",
    vmin=0,
    vmax=4  # Valor máximo (Consultancy=4, Search=4)
)

ax_c.set_xticks(np.arange(len(heatmap_regions)))
ax_c.set_xticklabels(
    heatmap_regions,
    rotation=35,
    ha="right",
    fontsize=15
)
ax_c.set_yticks(np.arange(len(heatmap_profiles)))
ax_c.set_yticklabels(heatmap_profiles, fontsize=15)

ax_c.set_title(
    "(c) Professional profile by region",
    loc="left", color=navy, fontweight="bold", pad=12, fontsize=18
)

for i in range(heatmap_data.shape[0]):
    for j in range(heatmap_data.shape[1]):
        value = heatmap_data[i, j]
        ax_c.text(
            j, i, str(value),
            ha="center", va="center",
            color="white" if value >= 3 else navy,
            fontweight="bold" if value > 0 else "normal",
            fontsize=16
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
cbar.set_label("Number of specialists", fontsize=15)

# ============================================================
# 7. PAINEL INFERIOR — IDENTIFICADORES DOS PARTICIPANTES
# ============================================================

ax_table.axis("off")

ax_table.text(
    0.01, 1.10,
    "Sample summary and participant traceability — Specialists who address the Clear Rules improvement (n=14)",
    fontsize=22,
    color=navy,
    fontweight="bold",
    va="top",
    transform=ax_table.transAxes
)

# Caixas de resumo
ax_table.text(
    0.01, 0.82,
    "TOTAL SAMPLE\n40 specialists",
    fontsize=16,
    color=navy,
    fontweight="bold",
    va="top",
    transform=ax_table.transAxes,
    bbox=dict(
        boxstyle="round,pad=0.6",
        facecolor=light_blue_box,
        edgecolor="#B8D6EC"
    )
)

ax_table.text(
    0.01, 0.52,
    "MENTION CLEAR RULES\nIMPROVEMENT\n14 specialists (35%)",
    fontsize=16,
    color=blue_improvement,
    fontweight="bold",
    va="top",
    transform=ax_table.transAxes,
    bbox=dict(
        boxstyle="round,pad=0.6",
        facecolor=light_blue_imp,
        edgecolor="#7BB5E2"
    )
)

df = pd.DataFrame(
    participants,
    columns=["Profile", "Region", "Participants (IDs)"]
)

# 12 linhas → 6 na esquerda, 6 na direita
df_left = df.iloc[:6]
df_right = df.iloc[6:]

def draw_table(ax, dataframe, bbox):
    table = ax.table(
        cellText=dataframe.values,
        colLabels=dataframe.columns,
        cellLoc="left",
        colLoc="left",
        bbox=bbox,
        colWidths=[0.35, 0.30, 0.55]
    )

    table.auto_set_font_size(False)
    table.set_fontsize(16)

    for (row, col), cell in table.get_celld().items():
        cell.set_edgecolor("#B8D6EC")
        cell.set_linewidth(0.7)
        cell.set_height(cell.get_height() * 1.15)

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

draw_table(
    ax_table,
    df_left,
    bbox=[0.28, 0.08, 0.34, 0.82]
)

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
path_png = os.path.join(script_dir, "clear_rules_improvement_three_panels.png")

plt.savefig(
    path_png,
    dpi=300,
    bbox_inches="tight"
)

plt.show()

print("Files saved:")
print(f"- {path_png}")