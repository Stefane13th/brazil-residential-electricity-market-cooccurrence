import os, re, itertools
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.path import Path
from matplotlib.patches import PathPatch
from matplotlib.lines import Line2D

# =============================================================================
#  DATA (IDs transcritos do Supplementary_data and Table 2 in arcticle)) 
# =============================================================================
def ids(s): return set(s.split())
TOPICS = {
 "Tariff Reduction": ("Opportunities", 22, ids("AS2 CA1 CA2 CT1 CT2 CT7 CT5 CT6 CT8 CP2 CP8 CP11 CP13 CP14 CP6 CP9 CP12 CP16 R3 R4 R5 U4")),
 "Supplier Flexibility": ("Opportunities", 14, ids("AS1 AS2 CT2 CT7 CT6 CT9 CP1 CP3 CP4 CP10 CP5 R3 R6 U3")),
 "Renewables": ("Opportunities", 9, ids("CA1 CT1 CT7 CT4 CT6 CP7 CP8 R2 R5")),
 "Innovation": ("Opportunities", 9, ids("AS3 CA2 CT3 CP6 CP9 CP15 CP7 CP14 R3")),
 "Modernization": ("Opportunities", 4, ids("CT6 R5 R6 U1")),
 "P2P": ("Opportunities", 3, ids("CA2 R2 U2")),
 "Regulatory Complexity": ("Barriers", 23, ids("AS2 AS3 CT1 CT2 CT3 CT8 CP1 CP3 CP6 CP12 CP15 CP16 CP2 CP5 CP7 CP11 CP13 R4 R5 R6 U1 U4 U2")),
 "Lack of Information": ("Barriers", 20, ids("AS2 AS3 CA2 CT2 CT7 CT4 CT5 CT6 CT8 CP4 CP9 CP15 CP16 CP7 CP8 R1 R4 R5 R6 R3")),
 "Distributor Impact": ("Barriers", 10, ids("AS1 AS3 CT8 CP2 CP11 CP12 CP15 CP16 R6 U1")),
 "Legacy Contracts": ("Barriers", 9, ids("AS1 AS2 AS3 CA2 CT2 CT3 CT8 R2 R5")),
 "Price Volatility": ("Barriers", 5, ids("CT1 CT2 CT9 CP10 CP16")), 
 "Smart Meter Costs": ("Barriers", 4, ids("CT6 CP14 CP15 R2")),
 "Digitalization & Technology": ("Improvements", 18, ids("CT1 CT5 CT6 CT9 CP1 CP9 CP10 CP15 CP16 CP2 CP5 CP7 CP8 CP11 R1 R4 R5 U2")),
 "Clear Rules": ("Improvements", 14, ids("AS3 CT3 CT4 CT7 CT8 CP14 CP12 R3 R4 R5 R6 U4 U2 U3")),
 "Consumer Info & Services": ("Improvements", 6, ids("CT2 CT6 CP1 CP4 CP6 CP15")),
 "Legislative Simplification": ("Improvements", 6, ids("AS1 AS2 CA2 CP3 CP10 U1")),
 "POLR": ("Improvements", 3, ids("AS1 AS2 AS3")),
 "Supply Guarantee": ("Improvements", 1, ids("CA1")),
}
GROUPS = {"CP":"Installers (CPi, n=16)","CT":"Consultancies (CTi, n=9)","R":"Researchers (Ri, n=6)",
          "U":"Utilities (Ui, n=4)","AS":"Associations (ASi, n=3)","CA":"Government (CAi, n=2)"}

# =============================================================================
# SETTINGS
# =============================================================================
FIGSIZE = (30, 22)
FONT_NODE = 22
FONT_EDGE = 22
PAD_PX = 14
EDGE_CLEAR_PX = 10
ITERATIONS = 1500
SEED = 3
MIN_WEIGHT_STK = 4
MIN_WEIGHT_TOPIC = 8
KEEP_ISOLATED = False

def grp(i): return re.match(r'[A-Z]+', i).group()

def generate_cooccurrence_network():
    G = nx.Graph()
    C = {"Opportunities": "#2ca02c", "Barriers": "#d62728",
         "Improvements": "#1f77b4", "Stakeholders": "#ff7f0e"}

    topics, stk_n = TOPICS, {k: sum(1 for t in TOPICS.values() for i in t[2] if grp(i) == k) for k in GROUPS}
    n_by_group = {"CP": 16, "CT": 9, "R": 6, "U": 4, "AS": 3, "CA": 2}
    def tlabel(name): return f"{name} (N={len(topics[name][2])})"
    raw = [(tlabel(t), g, len(ids_)) for t, (g, _, ids_) in topics.items()]
    raw += [(GROUPS[k], "Stakeholders", n_by_group[k]) for k in GROUPS]
    for lab, g, n in raw:
        G.add_node(lab, color=C[g], size=400 + n * 35, group=g)

    edges_data = []
    for t, (g, _, ids_) in topics.items():
        for k in GROUPS:
            w = sum(1 for i in ids_ if grp(i) == k)
            if w >= MIN_WEIGHT_STK: edges_data.append((GROUPS[k], tlabel(t), w))
    for (a_, (_, _, sa)), (b_, (_, _, sb)) in itertools.combinations(topics.items(), 2):
        w = len(sa & sb)
        if w >= MIN_WEIGHT_TOPIC: edges_data.append((tlabel(a_), tlabel(b_), w))
    for u, v, w in edges_data:
        G.add_edge(u, v, weight=w)
    if not KEEP_ISOLATED:
        G.remove_nodes_from(list(nx.isolates(G)))

    fig, ax = plt.subplots(figsize=FIGSIZE, facecolor="white")
    W, H = FIGSIZE
    ax.set_xlim(-W / 2, W / 2); ax.set_ylim(-H / 2, H / 2)
    ax.set_position([0.01, 0.01, 0.98, 0.92]); ax.axis("off")

    p0 = nx.kamada_kawai_layout(G)
    nodes = list(G.nodes)
    P = np.array([p0[n] for n in nodes])
    P = (P - (P.max(0) + P.min(0)) / 2) / ((P.max(0) - P.min(0)) / 2)
    P = P * np.array([W / 2 * 0.86, H / 2 * 0.84])

    texts = {}
    for n in nodes:
        texts[n] = ax.text(0, 0, n, fontsize=FONT_NODE,
                           fontweight="bold" if G.nodes[n]["group"] == "Stakeholders" else "normal",
                           ha="center", va="center", zorder=10,
                           bbox=dict(boxstyle="round,pad=0.35", fc="white",
                                     ec=G.nodes[n]["color"], lw=2, alpha=0.97))
    fig.canvas.draw()
    r = fig.canvas.get_renderer()
    half = np.array([[texts[n].get_bbox_patch().get_window_extent(r).width / 2,
                      texts[n].get_bbox_patch().get_window_extent(r).height / 2] for n in nodes])

    T = ax.transData
    X = T.transform(P)
    X0 = X.copy()
    idx = {n: i for i, n in enumerate(nodes)}
    E = [(idx[u], idx[v]) for u, v in G.edges]
    bx0, by0, bx1, by1 = ax.get_window_extent().extents
    rng = np.random.default_rng(SEED)
    X += rng.normal(0, 1, X.shape)

    for it in range(ITERATIONS):
        F = np.zeros_like(X)
        for i in range(len(nodes)):
            for j in range(i + 1, len(nodes)):
                d = X[j] - X[i]
                ox = half[i, 0] + half[j, 0] + PAD_PX - abs(d[0])
                oy = half[i, 1] + half[j, 1] + PAD_PX - abs(d[1])
                if ox > 0 and oy > 0:
                    if oy < ox:
                        s = np.sign(d[1]) or rng.choice([-1, 1]); F[i, 1] -= s * oy / 2; F[j, 1] += s * oy / 2
                    else:
                        s = np.sign(d[0]) or rng.choice([-1, 1]); F[i, 0] -= s * ox / 2; F[j, 0] += s * ox / 2
        for a, b in E:
            A, B = X[a], X[b]
            AB = B - A; L2 = AB @ AB
            if L2 < 1: continue
            for k in range(len(nodes)):
                if k in (a, b): continue
                t = np.clip((X[k] - A) @ AB / L2, 0.0, 1.0)
                Q = A + t * AB
                d = X[k] - Q
                dist = np.hypot(*d)
                n = d / dist if dist > 1e-6 else np.array([-AB[1], AB[0]]) / np.sqrt(L2)
                ext = abs(n[0]) * half[k, 0] + abs(n[1]) * half[k, 1] + EDGE_CLEAR_PX
                if dist < ext and 0.02 < t < 0.98:
                    push = (ext - dist) * 0.5
                    F[k] += n * push
                    F[a] -= n * push * 0.15 * (1 - t); F[b] -= n * push * 0.15 * t
        F += (X0 - X) * 0.004
        X += np.clip(F, -25, 25) * 0.6
        X[:, 0] = np.clip(X[:, 0], bx0 + half[:, 0] + 10, bx1 - half[:, 0] - 10)
        X[:, 1] = np.clip(X[:, 1], by0 + half[:, 1] + 10, by1 - half[:, 1] - 10)

    P = T.inverted().transform(X)
    pos = {n: P[idx[n]] for n in nodes}
    for n in nodes:
        texts[n].set_position(pos[n])

    # =================================================================
    # CORRECT ORDER OF PLOTTING:
    # 1. Colored circles (zorder=1) - FIRST (background)
    # 2. Edges (zorder=2 and zorder=3) - SECOND
    # 3. Edge weights (zorder=8) - THIRD
    # 4. Text boxes (zorder=10) - LAST (top)
    # =================================================================
    
    # 1. DRAW COLORED CIRCLES (zorder=1)
    for n in nodes:
        ax.scatter(*pos[n], s=G.nodes[n]["size"] * 6.0, c=G.nodes[n]["color"],
                   edgecolors="white", linewidths=7.0, alpha=1.0, zorder=1)

    # 2. DRAW EDGES
    RAD = 0.12
    def bez(u, v, t, curved):
        a, b = np.array(pos[u]), np.array(pos[v])
        if not curved: return a + t * (b - a)
        m = (a + b) / 2; d = b - a
        c = m + RAD * np.array([d[1], -d[0]]) * 2
        return (1 - t) ** 2 * a + 2 * (1 - t) * t * c + t ** 2 * b, c

    for u, v, d in G.edges(data=True):
        w = d["weight"]; curved = w < 4
        a, b = np.array(pos[u]), np.array(pos[v])
        if curved:
            _, c = bez(u, v, 0.5, True)
            patch = PathPatch(Path([a, c, b], [Path.MOVETO, Path.CURVE3, Path.CURVE3]), fill=False,
                              ec="#888888", lw=2.2, ls="--", alpha=0.75, zorder=2)
        else:
            patch = PathPatch(Path([a, b], [Path.MOVETO, Path.LINETO]), fill=False,
                              ec="#333333", lw=7.0, alpha=0.85, zorder=3)
        ax.add_patch(patch)

    # 3. EDGE WEIGHTS (zorder=8)
    node_px = {n: (X[idx[n]], half[idx[n]]) for n in nodes}
    placed = []
    ew, eh = FONT_EDGE * 1.1, FONT_EDGE * 1.2
    dpi = fig.dpi; ew *= dpi / 72 * 0.9; eh *= dpi / 72 * 0.9
    order = sorted(G.edges(data=True), key=lambda e: -e[2]["weight"])
    for u, v, d in order:
        curved = d["weight"] < 4
        best, bscore = None, 1e18
        for t in [0.5, 0.42, 0.58, 0.34, 0.66, 0.26, 0.74, 0.18, 0.82]:
            pt = bez(u, v, t, True)[0] if curved else bez(u, v, t, False)
            px = T.transform(pt)
            score = abs(t - 0.5) * 20
            for n, (c, h) in node_px.items():
                if abs(px[0] - c[0]) < h[0] + ew and abs(px[1] - c[1]) < h[1] + eh: score += 1e4
            for q in placed:
                if abs(px[0] - q[0]) < 2 * ew and abs(px[1] - q[1]) < 2 * eh: score += 1e3
            if score < bscore: best, bscore, bpt = px, score, pt
        placed.append(best)
        ax.text(*bpt, str(d["weight"]), fontsize=FONT_EDGE, fontweight="bold", color="#222222",
                ha="center", va="center", zorder=8,
                bbox=dict(boxstyle="round,pad=0.18", fc="white", ec="#aaaaaa", lw=0.8, alpha=0.95))

    # 4. TEXT BOXES FOR NODES (zorder=10) - have already been positioned above
    # Update positions of text boxes
    for n in nodes:
        texts[n].set_position(pos[n])

    # Legend and title
    leg = [Line2D([], [], marker='o', color='w', label='Opportunities', markerfacecolor=C["Opportunities"], markersize=25),
           Line2D([], [], marker='o', color='w', label='Barriers', markerfacecolor=C["Barriers"], markersize=25),
           Line2D([], [], marker='o', color='w', label='Improvements', markerfacecolor=C["Improvements"], markersize=25),
           Line2D([], [], marker='o', color='w', label='Stakeholders (Table 2)', markerfacecolor=C["Stakeholders"], markersize=25),
           Line2D([], [], color='#333333', lw=5.0, label=f'Co-occurrence (stakeholder–theme ≥ {MIN_WEIGHT_STK}; theme–theme ≥ {MIN_WEIGHT_TOPIC})')]
    ax.legend(handles=leg, loc="upper left", frameon=True, facecolor="white", edgecolor="#cccccc",
              fontsize=22, framealpha=1, borderpad=0.8).set_zorder(20)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(script_dir, "energy_cooccurrence_network.png")
    plt.savefig(filename, dpi=200, bbox_inches="tight")
    print(f"Graph successfully generated and saved as '{filename}'!")

if __name__ == "__main__":
    generate_cooccurrence_network()