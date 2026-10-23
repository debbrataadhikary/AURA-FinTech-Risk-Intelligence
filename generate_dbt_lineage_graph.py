"""
AURA FinTech Risk Intelligence - dbt Medallion DAG Lineage Graph Generator
Generates a production-grade, high-resolution lineage DAG image matching the
dbt documentation lineage interface aesthetic (dark teal canvas, pill nodes, bezier curves).
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.path import Path
import numpy as np

def create_lineage_graph(output_path="assets/dbt_project_lineage.png"):
    fig, ax = plt.subplots(figsize=(18, 9), dpi=300)
    bg_color = "#084152"  # Exact dbt docs dark teal
    fig.patch.set_facecolor(bg_color)
    ax.set_facecolor(bg_color)
    ax.set_xlim(0, 18)
    ax.set_ylim(0, 9)
    ax.axis("off")

    # Header Title
    ax.text(0.6, 8.4, "Lineage Graph", fontsize=16, fontweight="bold", color="#FFFFFF", fontfamily="sans-serif")
    ax.text(0.6, 8.0, "AURA FinTech Medallion DAG (Bronze Raw -> Staging -> Silver Intermediate -> Gold Marts)", 
            fontsize=10, color="#7DD3FC", fontfamily="sans-serif")

    # Node definitions: (name, x, y, width, height, fill_color, border_color, text_color)
    # Colors:
    # Source Credit: Magenta #A21CAF
    # Source Stream: Green #16A34A
    # Source Macro: Amber #D97706
    # Models: Teal #0E7490 with border #06B6D4
    nodes = {
        # Sources (Layer 0)
        "src_credit": {"name": "aura_raw.fact_credit_portfolio", "x": 0.5, "y": 6.2, "w": 3.2, "h": 0.55, "bg": "#9333EA", "bdr": "#C084FC", "txt": "#FFFFFF"},
        "src_stream": {"name": "aura_raw.fact_transactions_stream", "x": 0.5, "y": 4.2, "w": 3.2, "h": 0.55, "bg": "#15803D", "bdr": "#4ADE80", "txt": "#FFFFFF"},
        "src_macro":  {"name": "aura_raw.dim_macro_stress_scenarios", "x": 0.5, "y": 2.2, "w": 3.2, "h": 0.55, "bg": "#B45309", "bdr": "#FBBF24", "txt": "#FFFFFF"},

        # Staging (Layer 1)
        "stg_credit": {"name": "stg_credit_portfolio", "x": 4.5, "y": 6.2, "w": 2.5, "h": 0.55, "bg": "#0E7490", "bdr": "#22D3EE", "txt": "#FFFFFF"},
        "stg_stream": {"name": "stg_transactions_stream", "x": 4.5, "y": 4.2, "w": 2.5, "h": 0.55, "bg": "#0E7490", "bdr": "#22D3EE", "txt": "#FFFFFF"},
        "stg_macro":  {"name": "stg_macro_scenarios", "x": 4.5, "y": 2.2, "w": 2.5, "h": 0.55, "bg": "#0E7490", "bdr": "#22D3EE", "txt": "#FFFFFF"},

        # Silver Intermediate (Layer 2)
        "int_credit": {"name": "int_credit_risk_staging", "x": 7.8, "y": 5.8, "w": 2.7, "h": 0.55, "bg": "#0E7490", "bdr": "#22D3EE", "txt": "#FFFFFF"},
        "int_aml":    {"name": "int_aml_behavioral_metrics", "x": 7.8, "y": 3.8, "w": 2.7, "h": 0.55, "bg": "#0E7490", "bdr": "#22D3EE", "txt": "#FFFFFF"},

        # Gold Fact Marts (Layer 3)
        "fct_ecl":    {"name": "fct_ifrs9_ecl_provisions", "x": 11.4, "y": 7.2, "w": 2.7, "h": 0.55, "bg": "#0E7490", "bdr": "#22D3EE", "txt": "#FFFFFF"},
        "fct_basel":  {"name": "fct_basel_iii_capital_adequacy", "x": 11.4, "y": 5.8, "w": 2.9, "h": 0.55, "bg": "#0E7490", "bdr": "#22D3EE", "txt": "#FFFFFF"},
        "fct_geo":    {"name": "fct_portfolio_country_risk", "x": 11.4, "y": 4.6, "w": 2.7, "h": 0.55, "bg": "#0E7490", "bdr": "#22D3EE", "txt": "#FFFFFF"},
        "fct_aml":    {"name": "fct_aml_forensic_watchlist", "x": 11.4, "y": 3.4, "w": 2.7, "h": 0.55, "bg": "#0E7490", "bdr": "#22D3EE", "txt": "#FFFFFF"},

        # Gold Downstream / Stress Testing (Layer 4)
        "fct_stress": {"name": "fct_macro_stress_testing_impact", "x": 15.0, "y": 5.0, "w": 2.7, "h": 0.55, "bg": "#0E7490", "bdr": "#22D3EE", "txt": "#FFFFFF"}
    }

    # Edges (Source, Target, Color)
    edges = [
        # Bronze -> Staging
        ("src_credit", "stg_credit", "#C084FC"),
        ("src_stream", "stg_stream", "#4ADE80"),
        ("src_macro", "stg_macro", "#FBBF24"),

        # Staging -> Silver
        ("stg_credit", "int_credit", "#E879F9"),
        ("stg_stream", "int_aml", "#22D3EE"),

        # Silver -> Gold
        ("int_credit", "fct_ecl", "#F472B6"),
        ("int_credit", "fct_basel", "#E879F9"),
        ("int_credit", "fct_geo", "#C084FC"),
        ("int_aml", "fct_aml", "#22D3EE"),

        # Cross-layer dependencies to Macro Stress Testing
        ("fct_basel", "fct_stress", "#E879F9"),
        ("stg_macro", "fct_stress", "#FBBF24")
    ]

    # Draw Edges as smooth Bezier curves
    for u, v, col in edges:
        n1 = nodes[u]
        n2 = nodes[v]
        x1 = n1["x"] + n1["w"]
        y1 = n1["y"] + n1["h"] / 2
        x2 = n2["x"]
        y2 = n2["y"] + n2["h"] / 2

        # Control points for smooth horizontal S-curve
        dx = x2 - x1
        c1x = x1 + dx * 0.5
        c1y = y1
        c2x = x1 + dx * 0.5
        c2y = y2

        verts = [(x1, y1), (c1x, c1y), (c2x, c2y), (x2, y2)]
        codes = [Path.MOVETO, Path.CURVE4, Path.CURVE4, Path.CURVE4]
        path = Path(verts, codes)
        patch = patches.PathPatch(path, facecolor="none", edgecolor=col, lw=2.0, alpha=0.85, zorder=1)
        ax.add_patch(patch)

        # Draw arrow at endpoint
        ax.annotate("", xy=(x2, y2), xytext=(x2 - 0.15, y2),
                    arrowprops=dict(arrowstyle="->", color=col, lw=2.0, mutation_scale=14), zorder=2)

    # Draw Nodes as rounded pill boxes with drop shadow
    for key, n in nodes.items():
        x, y, w, h = n["x"], n["y"], n["w"], n["h"]
        
        # Shadow
        shadow = patches.FancyBboxPatch(
            (x + 0.04, y - 0.04), w, h,
            boxstyle="round,pad=0.08,rounding_size=0.15",
            facecolor="#04222B", edgecolor="none", alpha=0.6, zorder=3
        )
        ax.add_patch(shadow)

        # Main box
        box = patches.FancyBboxPatch(
            (x, y), w, h,
            boxstyle="round,pad=0.08,rounding_size=0.15",
            facecolor=n["bg"], edgecolor=n["bdr"], lw=1.5, zorder=4
        )
        ax.add_patch(box)

        # Node text
        ax.text(
            x + w / 2, y + h / 2, n["name"],
            ha="center", va="center", color=n["txt"],
            fontsize=9.5, fontweight="semibold", fontfamily="sans-serif", zorder=5
        )

    # Legend / Badges at bottom
    legend_items = [
        ("Raw Sources (Bronze)", "#9333EA", "#C084FC"),
        ("Staging Models (Silver-L1)", "#0E7490", "#22D3EE"),
        ("Intermediate Features (Silver-L2)", "#0E7490", "#E879F9"),
        ("Reporting Marts (Gold Fact)", "#0E7490", "#F472B6"),
        ("Macro Shock Engine", "#0E7490", "#FBBF24")
    ]
    leg_x = 1.0
    for title, fill_c, edge_c in legend_items:
        lbox = patches.FancyBboxPatch(
            (leg_x, 0.4), 0.35, 0.25,
            boxstyle="round,pad=0.04,rounding_size=0.08",
            facecolor=fill_c, edgecolor=edge_c, lw=1.2, zorder=4
        )
        ax.add_patch(lbox)
        ax.text(leg_x + 0.45, 0.52, title, color="#CBD5E1", fontsize=9, va="center", fontfamily="sans-serif")
        leg_x += 3.3

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, facecolor=fig.get_facecolor(), bbox_inches="tight")
    plt.close()
    print(f"Lineage graph saved successfully to {output_path}")

if __name__ == "__main__":
    create_lineage_graph()
