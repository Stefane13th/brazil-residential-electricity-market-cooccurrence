
import os
import re
import itertools
import numpy as np
from collections import defaultdict, Counter

# =============================================================================
# DATA (same as in the main code)
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

GROUPS = {"CP": "Installers", "CT": "Consultancies", "R": "Researchers",
          "U": "Utilities", "AS": "Associations", "CA": "Government"}

n_by_group = {"CP": 16, "CT": 9, "R": 6, "U": 4, "AS": 3, "CA": 2}


def get_group_prefix(i): return re.match(r'[A-Z]+', i).group()


# =============================================================================
# 1. THRESHOLD SENSITIVITY ANALYSIS
# =============================================================================
def analyze_sensitivity():
    print("="*70)
    print("📊 THRESHOLD SENSITIVITY ANALYSIS")
    print("="*70)

    # Tests different threshold combinations
    stakeholder_thresholds = [2, 3, 4, 5, 6]
    topic_thresholds = [3, 4, 5, 6, 7, 8]

    print("\n🔹 Stakeholder-Theme Edges by Threshold:")
    print(f"{'Threshold':<12} {'Edges':<10} {'% of total'}")
    print("-"*40)

    total_stakeholder_edges = 0
    for min_weight in stakeholder_thresholds:
        count = 0
        for topic, (category, _, topic_ids) in TOPICS.items():
            for group in GROUPS:
                weight = sum(1 for i in topic_ids if get_group_prefix(i) == group)
                if weight >= min_weight:
                    count += 1
        total_stakeholder_edges = max(total_stakeholder_edges, count)
        percentage = (count / (len(TOPICS) * len(GROUPS))) * 100
        marker = " ← CURRENT" if min_weight == 4 else ""
        print(f"{min_weight:<12} {count:<10} {percentage:.1f}%{marker}")

    print("\n🔹 Theme-Theme Edges by Threshold:")
    print(f"{'Threshold':<12} {'Edges':<10} {'% of total'}")
    print("-"*40)

    for min_weight in topic_thresholds:
        count = 0
        for (a, (_, _, set_a)), (b, (_, _, set_b)) in itertools.combinations(TOPICS.items(), 2):
            weight = len(set_a & set_b)
            if weight >= min_weight:
                count += 1
        total_pairs = len(list(itertools.combinations(TOPICS.items(), 2)))
        percentage = (count / total_pairs) * 100
        marker = " ← CURRENT" if min_weight == 8 else ""
        print(f"{min_weight:<12} {count:<10} {percentage:.1f}%{marker}")


# =============================================================================
# 2. ALTERNATIVE SIMILARITY MEASURES
# =============================================================================
def similarity_measures():
    print("\n" + "="*70)
    print("📐 SIMILARITY MEASURES BETWEEN THEMES (Top 15 pairs)")
    print("="*70)

    results = []
    for (a, (_, _, set_a)), (b, (_, _, set_b)) in itertools.combinations(TOPICS.items(), 2):
        intersection = len(set_a & set_b)
        union = len(set_a | set_b)

        # Raw co-occurrence (current measure)
        cooccurrence = intersection

        # Jaccard index (0 to 1)
        jaccard = intersection / union if union > 0 else 0

        # Phi coefficient (correlation for binary variables)
        # a=both, b=only A, c=only B, d=neither
        a_count = intersection
        b_count = len(set_a) - intersection
        c_count = len(set_b) - intersection
        d_count = 40 - a_count - b_count - c_count  # total number of experts

        denominator = np.sqrt((a_count+b_count)*(a_count+c_count)*(b_count+d_count)*(c_count+d_count))
        phi = (a_count*d_count - b_count*c_count) / denominator if denominator > 0 else 0

        # Overlap coefficient (Szymkiewicz-Simpson)
        overlap = intersection / min(len(set_a), len(set_b)) if min(len(set_a), len(set_b)) > 0 else 0

        results.append({
            'pair': f"{a} ↔ {b}",
            'cooccurrence': cooccurrence,
            'jaccard': jaccard,
            'phi': phi,
            'overlap': overlap
        })

    # Sort by co-occurrence
    results.sort(key=lambda x: -x['cooccurrence'])

    print(f"\n{'Theme pair':<60} {'Co-occ.':<6} {'Jaccard':<10} {'Phi':<8} {'Overlap':<10}")
    print("-"*100)

    for result in results[:15]:
        print(f"{result['pair']:<60} {result['cooccurrence']:<6} {result['jaccard']:<10.3f} {result['phi']:<8.3f} {result['overlap']:<10.3f}")

    return results



# =============================================================================
# 3. BOOTSTRAP VALIDATION (edge stability)
# =============================================================================
def validate_bootstrap(n_iterations=1000, seed=42):

    print("\n" + "="*70)
    print(f"BOOTSTRAP VALIDATION ({n_iterations} iterations)")
    print("="*70)
    print("Resampling 40 experts with replacement to assess network edge stability.\n")

    # Reconstructs the complete list of 40 experts
    experts = [
        f"{prefix}{i}"
        for prefix, n in n_by_group.items()
        for i in range(1, n + 1)
    ]

    if len(experts) != 40:
        raise ValueError("The dataset must contain exactly 40 experts.")

    expert_set = set(experts)

    # Checks whether all topic identifiers belong to the sample
    all_topic_ids = set().union(
        *(data[2] for data in TOPICS.values())
    )

    unknown_ids = all_topic_ids - expert_set

    if unknown_ids:
        raise ValueError(
            f"Unknown expert identifiers found: {unknown_ids}"
        )

    # Reproducible random number generator
    rng = np.random.default_rng(seed)

    # Thresholds used in the original network
    stakeholder_threshold = 4
    topic_threshold = 8

    # -------------------------------------------------------------------------
    # IDENTIFY THE ORIGINAL NETWORK EDGES
    # -------------------------------------------------------------------------
    edges = []

    # Stakeholder-theme edges
    for topic, (_, _, topic_ids) in TOPICS.items():

        for prefix, group_name in GROUPS.items():

            members = {
                expert for expert in topic_ids
                if get_group_prefix(expert) == prefix
            }

            original_weight = len(members)

            if original_weight >= stakeholder_threshold:

                edges.append({
                    "type": "Profile-Theme",
                    "node_1": group_name,
                    "node_2": topic,
                    "original_weight": original_weight,
                    "threshold": stakeholder_threshold,
                    "members": members
                })

    # Theme-theme edges
    for (topic_a, (_, _, set_a)), \
        (topic_b, (_, _, set_b)) in itertools.combinations(
            TOPICS.items(), 2
        ):

        shared_experts = set_a & set_b
        original_weight = len(shared_experts)

        if original_weight >= topic_threshold:

            edges.append({
                "type": "Theme-Theme",
                "node_1": topic_a,
                "node_2": topic_b,
                "original_weight": original_weight,
                "threshold": topic_threshold,
                "members": shared_experts
            })

    print(f"Original network edges: {len(edges)}")
    print("Starting bootstrap resampling...\n")

    # -------------------------------------------------------------------------
    # BOOTSTRAP RESAMPLING
    # -------------------------------------------------------------------------
    edge_frequency = np.zeros(len(edges), dtype=int)

    for iteration in range(n_iterations):

        # Samples 40 experts with replacement
        sampled_experts = rng.choice(
            experts,
            size=40,
            replace=True
        )

        # Counts how many times each expert was sampled
        sample_counts = Counter(sampled_experts)

        # Recalculates every original network edge
        for edge_index, edge in enumerate(edges):

            # Counts the sampled occurrences of the experts
            # belonging to the respective edge
            new_weight = sum(
                sample_counts[expert]
                for expert in edge["members"]
            )

            # Checks whether the edge remains in the network
            if new_weight >= edge["threshold"]:
                edge_frequency[edge_index] += 1

    # -------------------------------------------------------------------------
    # CALCULATE EDGE INCLUSION FREQUENCY
    # -------------------------------------------------------------------------
    results = []

    for index, edge in enumerate(edges):

        stability = (
            edge_frequency[index] / n_iterations
        ) * 100

        results.append({
            "type": edge["type"],
            "edge": f'{edge["node_1"]} <-> {edge["node_2"]}',
            "original_weight": edge["original_weight"],
            "bootstrap_frequency": edge_frequency[index],
            "stability": stability
        })

    # Sorts edges by bootstrap inclusion frequency
    results.sort(
        key=lambda x: x["stability"],
        reverse=True
    )

    # -------------------------------------------------------------------------
    # DISPLAY RESULTS
    # -------------------------------------------------------------------------
    print(
        f"{'Type':<16} "
        f"{'Edge':<65} "
        f"{'Original':<10} "
        f"{'Frequency':<12} "
        f"{'Stability':<10}"
    )

    print("-"*115)

    for result in results:

        print(
            f"{result['type']:<16} "
            f"{result['edge']:<65} "
            f"{result['original_weight']:<10} "
            f"{result['bootstrap_frequency']:<12} "
            f"{result['stability']:.1f}%"
        )

    return results


# =============================================================================
# 4. CENTRALITY ANALYSIS (identifying the actual hubs)
# =============================================================================
def analyze_centrality():
    print("\n" + "="*70)
    print("🎯 NODE CENTRALITY ANALYSIS")
    print("="*70)

    # Calculates the degree (number of connections) of each stakeholder
    print("\n🔹 Stakeholder Degree Centrality:")
    print(f"{'Stakeholder':<30} {'Connections (degree)':<18} {'Total weight':<12}")
    print("-"*60)

    stakeholder_degree = defaultdict(lambda: {'degree': 0, 'weight': 0})

    for topic, (category, _, topic_ids) in TOPICS.items():
        for group in GROUPS:
            weight = sum(1 for i in topic_ids if get_group_prefix(i) == group)
            if weight >= 4:  # current threshold
                stakeholder_degree[GROUPS[group]]['degree'] += 1
                stakeholder_degree[GROUPS[group]]['weight'] += weight

    for stakeholder, data in sorted(stakeholder_degree.items(), key=lambda x: -x[1]['weight']):
        print(f"{stakeholder:<30} {data['degree']:<18} {data['weight']:<12}")


# =============================================================================
# 5. COMPLETE CO-OCCURRENCE MATRIX (for additional analysis)
# =============================================================================
def cooccurrence_matrix():
    print("\n" + "="*70)
    print("📋 THEME x THEME CO-OCCURRENCE MATRIX (raw values)")
    print("="*70)

    themes = list(TOPICS.keys())
    matrix = np.zeros((len(themes), len(themes)), dtype=int)

    for i, (a, (_, _, set_a)) in enumerate(TOPICS.items()):
        for j, (b, (_, _, set_b)) in enumerate(TOPICS.items()):
            if i != j:
                matrix[i, j] = len(set_a & set_b)

    # Displays only pairs with co-occurrence >= 4
    print("\nPairs with co-occurrence ≥ 4:")
    pairs = []

    for i in range(len(themes)):
        for j in range(i+1, len(themes)):
            if matrix[i, j] >= 4:
                pairs.append((themes[i], themes[j], matrix[i, j]))

    pairs.sort(key=lambda x: -x[2])

    for a, b, weight in pairs:
        print(f"  {a:<35} ↔ {b:<35} = {weight}")


# =============================================================================
# RUN ALL VALIDATION PROCEDURES
# =============================================================================
if __name__ == "__main__":
    analyze_sensitivity()
    similarity_measures()
    validate_bootstrap(n_iterations=1000, seed=42)
    analyze_centrality()
    cooccurrence_matrix()

    print("\n" + "="*70)
    print("✅ VALIDATION COMPLETED!")
    print("="*70)
    print("\n💡 Recommendations:")
    print("    increasing the threshold or reporting only robust edges.")
    print("  • Use the Jaccard index to compare themes of different sizes.")
    print("  • The Phi coefficient indicates the statistical correlation between themes.")
