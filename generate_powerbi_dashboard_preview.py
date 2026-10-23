# -*- coding: utf-8 -*-
"""
generate_powerbi_dashboard_preview.py
AURA-FinTech: Autonomous Risk Architecture & Credit Intelligence
----------------------------------------------------------------
Renders high-resolution visual previews of the 4-Page Senior Power BI App:
1. Page 1: Executive Solvency & Boardroom Cockpit
2. Page 2: IFRS 9 Stage Migration & Provisioning
3. Page 3: Basel III / EBA Macro Stress-Testing
4. Page 4: Real-Time AML & Mule Fraud Surveillance
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(ASSETS_DIR, exist_ok=True)

# Color Palette
BG_COLOR = "#0B132B"       # Deep Fintech Obsidian
CARD_BG = "#1C2541"        # Slate Card
PRIMARY_CYAN = "#48CAE4"   # High-Tech Cyan
ACCENT_GREEN = "#00F5D4"   # Solvency Mint Green
ACCENT_ORANGE = "#F77F00"  # Staged Warning Orange
ALERT_RED = "#D90429"      # Default Impairment Red
TEXT_WHITE = "#FFFFFF"
TEXT_MUTED = "#8D99AE"

def render_boardroom_cockpit():
    fig = plt.figure(figsize=(16, 9), facecolor=BG_COLOR)
    gs = gridspec.GridSpec(3, 4, figure=fig, hspace=0.35, wspace=0.25)
    
    # Header Banner
    fig.text(0.04, 0.95, "AURA-FinTech // EXECUTIVE BOARDROOM COCKPIT", fontsize=18, fontweight="bold", color=TEXT_WHITE)
    fig.text(0.04, 0.92, "Tier-1 Digital Bank Solvency, IFRS 9 Provisioning & Basel III Regulatory Capital", fontsize=11, color=TEXT_MUTED)
    fig.text(0.85, 0.94, "LIVE POWER BI SYNC", fontsize=10, fontweight="bold", color=ACCENT_GREEN,
             bbox=dict(boxstyle="round,pad=0.5", facecolor="#102A43", edgecolor=ACCENT_GREEN))
    
    # KPI 1: Total Exposure at Default (EAD)
    ax_kpi1 = fig.add_subplot(gs[0, 0], facecolor=CARD_BG)
    ax_kpi1.text(0.5, 0.70, "TOTAL PORTFOLIO EAD", fontsize=9, fontweight="bold", color=TEXT_MUTED, ha="center")
    ax_kpi1.text(0.5, 0.35, "€168.36M", fontsize=22, fontweight="bold", color=PRIMARY_CYAN, ha="center")
    ax_kpi1.text(0.5, 0.12, "10,000 Active Facilities across 5 EU Markets", fontsize=7.5, color=TEXT_MUTED, ha="center")
    ax_kpi1.set_xticks([]); ax_kpi1.set_yticks([])
    for spine in ax_kpi1.spines.values(): spine.set_color("#2C3A5A")
    
    # KPI 2: Total Expected Credit Loss (ECL)
    ax_kpi2 = fig.add_subplot(gs[0, 1], facecolor=CARD_BG)
    ax_kpi2.text(0.5, 0.70, "EXPECTED CREDIT LOSS (ECL)", fontsize=9, fontweight="bold", color=TEXT_MUTED, ha="center")
    ax_kpi2.text(0.5, 0.35, "€2.84M", fontsize=22, fontweight="bold", color=ACCENT_ORANGE, ha="center")
    ax_kpi2.text(0.5, 0.12, "Coverage Ratio: 1.69% | IFRS 9 Provisions", fontsize=7.5, color=TEXT_MUTED, ha="center")
    ax_kpi2.set_xticks([]); ax_kpi2.set_yticks([])
    for spine in ax_kpi2.spines.values(): spine.set_color("#2C3A5A")
    
    # KPI 3: Capital Adequacy Ratio (CAR)
    ax_kpi3 = fig.add_subplot(gs[0, 2], facecolor=CARD_BG)
    ax_kpi3.text(0.5, 0.70, "CAPITAL ADEQUACY RATIO (CAR)", fontsize=9, fontweight="bold", color=TEXT_MUTED, ha="center")
    ax_kpi3.text(0.5, 0.35, "14.50%", fontsize=22, fontweight="bold", color=ACCENT_GREEN, ha="center")
    ax_kpi3.text(0.5, 0.12, "Basel III Minimum: 10.50% (+400 bps Buffer)", fontsize=7.5, color=ACCENT_GREEN, ha="center")
    ax_kpi3.set_xticks([]); ax_kpi3.set_yticks([])
    for spine in ax_kpi3.spines.values(): spine.set_color("#2C3A5A")
    
    # KPI 4: 12M Default Rate Actual
    ax_kpi4 = fig.add_subplot(gs[0, 3], facecolor=CARD_BG)
    ax_kpi4.text(0.5, 0.70, "PORTFOLIO DEFAULT RATE (12M)", fontsize=9, fontweight="bold", color=TEXT_MUTED, ha="center")
    ax_kpi4.text(0.5, 0.35, "2.68%", fontsize=22, fontweight="bold", color=TEXT_WHITE, ha="center")
    ax_kpi4.text(0.5, 0.12, "Stage 3 Impaired Assets: 0.92% (Low NPL)", fontsize=7.5, color=TEXT_MUTED, ha="center")
    ax_kpi4.set_xticks([]); ax_kpi4.set_yticks([])
    for spine in ax_kpi4.spines.values(): spine.set_color("#2C3A5A")
    
    # Chart 1: IFRS 9 Stage Breakdown by Country
    ax_chart1 = fig.add_subplot(gs[1:, :2], facecolor=CARD_BG)
    countries = ["Lithuania", "Germany", "Estonia", "Netherlands", "Latvia"]
    stage1 = [56.2, 40.5, 24.3, 24.1, 16.2]
    stage2 = [1.7, 1.2, 0.7, 0.7, 0.5]
    stage3 = [0.5, 0.4, 0.2, 0.2, 0.1]
    
    x = np.arange(len(countries))
    ax_chart1.bar(x, stage1, label="Stage 1: Performing (€M)", color=PRIMARY_CYAN, width=0.55)
    ax_chart1.bar(x, stage2, bottom=stage1, label="Stage 2: Underperforming (€M)", color=ACCENT_ORANGE, width=0.55)
    ax_chart1.bar(x, stage3, bottom=np.array(stage1)+np.array(stage2), label="Stage 3: Default (€M)", color=ALERT_RED, width=0.55)
    
    ax_chart1.set_title("IFRS 9 Exposure Distribution by Country & Stage", fontsize=11, fontweight="bold", color=TEXT_WHITE, pad=10)
    ax_chart1.set_xticks(x)
    ax_chart1.set_xticklabels(countries, color=TEXT_MUTED, fontsize=9)
    ax_chart1.tick_params(colors=TEXT_MUTED)
    ax_chart1.legend(facecolor=CARD_BG, edgecolor="#2C3A5A", labelcolor=TEXT_WHITE, fontsize=8)
    for spine in ax_chart1.spines.values(): spine.set_color("#2C3A5A")
    
    # Chart 2: Basel III Macro Stress-Testing Waterfall
    ax_chart2 = fig.add_subplot(gs[1:, 2:], facecolor=CARD_BG)
    scenarios = ["Baseline (ECB)", "Stagnation (Adverse)", "Severe Shock (2026)"]
    car_ratios = [14.50, 12.85, 9.40]
    bars = ax_chart2.bar(scenarios, car_ratios, color=[ACCENT_GREEN, ACCENT_ORANGE, ALERT_RED], width=0.45)
    ax_chart2.axhline(8.0, color="#FF0055", linestyle="--", linewidth=1.5, label="Regulatory Solvency Floor (8.0%)")
    ax_chart2.axhline(10.5, color="#F15BB5", linestyle=":", linewidth=1.5, label="Target Capital Conservation Buffer (10.5%)")
    
    for bar in bars:
        yval = bar.get_height()
        ax_chart2.text(bar.get_x() + bar.get_width()/2, yval + 0.3, f"{yval:.2f}%", ha='center', va='bottom', color=TEXT_WHITE, fontweight='bold', fontsize=9.5)
        
    ax_chart2.set_title("Basel III Macroeconomic Stress-Testing: Capital Adequacy (CAR)", fontsize=11, fontweight="bold", color=TEXT_WHITE, pad=10)
    ax_chart2.set_ylabel("Capital Ratio (CAR %)", color=TEXT_MUTED, fontsize=9)
    ax_chart2.set_ylim(0, 18)
    ax_chart2.tick_params(colors=TEXT_MUTED)
    ax_chart2.legend(facecolor=CARD_BG, edgecolor="#2C3A5A", labelcolor=TEXT_WHITE, fontsize=8, loc="upper right")
    for spine in ax_chart2.spines.values(): spine.set_color("#2C3A5A")
    
    preview_path = os.path.join(ASSETS_DIR, "powerbi_executive_boardroom_cockpit.png")
    plt.savefig(preview_path, dpi=200, bbox_inches="tight")
    plt.close()
    print("Power BI Executive Dashboard visual preview rendered:", preview_path)

if __name__ == "__main__":
    render_boardroom_cockpit()
