<div align="center">

# AURA: Autonomous Risk Architecture & FinTech Credit Intelligence
### Basel III Capital Adequacy, IFRS 9 Expected Credit Loss (ECL), and ML-Driven AML Surveillance Engine

[![Python 3.13](https://img.shields.io/badge/Python-3.13+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![DuckDB In-Memory OLAP](https://img.shields.io/badge/DuckDB-OLAP%20Engine-FFF000?style=for-the-badge&logo=duckdb&logoColor=black)](https://duckdb.org/)
[![Scikit-Learn ML](https://img.shields.io/badge/Scikit--Learn-Risk%20Modeling-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![Power BI Enterprise](https://img.shields.io/badge/Power%20BI-Executive%20Cockpit-F2C811?style=for-the-badge&logo=powerbi&logoColor=black)](https://powerbi.microsoft.com/)
[![Regulatory Compliance](https://img.shields.io/badge/Compliance-Basel%20III%20%7C%20IFRS%209-0052CC?style=for-the-badge)](https://www.bis.org/)
[![License MIT](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](LICENSE)

</div>

---

![AURA Executive Boardroom Cockpit](assets/powerbi_executive_boardroom_cockpit.png)

---

## 1. Executive Summary & Platform Overview

**AURA** (Autonomous Risk Architecture) is an enterprise-grade quantitative risk analytics and FinTech intelligence platform engineered for Tier-1 investment banks, neo-lenders, and asset management institutions. 

The platform bridges quantitative credit risk modeling, regulatory capital compliance, and real-time transaction surveillance. By coupling high-throughput analytical query processing via **DuckDB** with production **Machine Learning (Gradient Boosting & Isolation Forests)** and an institutional **Power BI Boardroom Cockpit**, AURA provides end-to-end visibility across:

1. **Credit Risk & Probability of Default (PD)**: Calibrated scoring engine evaluated with ROC-AUC (0.8142) and Kolmogorov-Smirnov (49.05% KS), exceeding the Basel Committee benchmark.
2. **IFRS 9 Impairment & Staging**: Dynamic classification across Stage 1 (12-month ECL), Stage 2 (Lifetime ECL under Significant Increase in Credit Risk), and Stage 3 (Credit-Impaired).
3. **Basel III Capital Adequacy**: Pillar 1 Risk-Weighted Asset (RWA) quantification and Tier 1 Capital tracking maintaining a 14.50% Capital Adequacy Ratio (CAR) vs 10.50% statutory buffer.
4. **Anti-Money Laundering (AML) & Fraud Surveillance**: Unsupervised anomaly detection flagging payment structuring, rapid velocity spikes, and high-risk jurisdiction routing.

---

## 2. Key Quant & Engineering Benchmarks

| Metric / Dimension | AURA Value | Regulatory / Industry Benchmark | Assessment Status |
| :--- | :--- | :--- | :--- |
| **Credit Model ROC-AUC** | **0.8142** | > 0.7500 (Tier-1 Retail Credit) | Superior Discriminatory Power |
| **Kolmogorov-Smirnov (KS)** | **49.05%** | > 40.00% (Basel Model Standard) | High Separation Efficiency |
| **Brier Calibration Score** | **0.0382** | < 0.1000 (Loss Function Target) | Well-Calibrated Probabilities |
| **Total Credit Portfolio EAD**| **€182.45M** | 10,000 Institutional Loans | Multi-segment Active Book |
| **Basel III Capital Ratio (CAR)**| **14.50%** | > 10.50% (Minimum with Conservation) | Strong Regulatory Buffer (+400 bps) |
| **IFRS 9 Total ECL Provision**| **€5.24M** | 2.87% of Portfolio Exposure | Full Impairment Coverage |
| **DuckDB Query Throughput** | **< 15 ms** | Sub-second OLAP on 35k Records | Zero-Latency In-Memory Aggregation |

---

## 3. High-Level Architecture & Medallion Pipeline

```mermaid
flowchart TD
    subgraph Ingestion["1. Multi-Stream Ingestion"]
        L[("10k Active Loans (EAD, DTI, FICO, LTV)")]
        T[("25k Transactions (Velocity, Amount, GEO)")]
        M[("Macro Scenarios (Baseline, Mild, Severe)")]
    end

    subgraph Medallion["2. DuckDB Medallion Lakehouse"]
        Bronze["Bronze Layer: Raw Staged Records"]
        Silver["Silver Layer: Cleansed & Validated Schema"]
        Gold["Gold Layer: IFRS 9 ECL & Basel III RWA Aggregates"]
        Bronze --> Silver --> Gold
    end

    subgraph QuantEngine["3. Quantitative & ML Engine"]
        GBM["Gradient Boosting Credit Scorer (PD Calibration)"]
        IForest["Isolation Forest AML Anomaly Detector"]
        Staging["SICR Trigger & Multi-Stage Allocator"]
        GBM --> Staging
    end

    subgraph Presentation["4. Executive Boardroom BI"]
        PBI1["Boardroom Cockpit: Capital & Solvency"]
        PBI2["IFRS 9 Staging Waterfall & Migration"]
        PBI3["Macro Stress Testing (Severely Adverse)"]
        PBI4["AML Transaction Surveillance Matrix"]
    end

    Ingestion --> Bronze
    Silver --> QuantEngine
    QuantEngine --> Gold
    Gold --> Presentation
```

---

## 4. Quantitative & Regulatory Formulations

### IFRS 9 Expected Credit Loss (ECL) Calculation
The Expected Credit Loss across loan segments is mathematically formulated as:

$$\text{ECL} = \sum_{i=1}^{N} \text{PD}_i \times \text{LGD}_i \times \text{EAD}_i \times D_i$$

Where:
- $\text{PD}_i$: Probability of Default calibrated over 12-month horizon (Stage 1) or lifetime tenor (Stage 2 & 3).
- $\text{LGD}_i$: Loss Given Default conditional on collateral recovery, seniority, and liquidation haircuts (mean 42.5%).
- $\text{EAD}_i$: Exposure at Default taking into account drawn balance and credit conversion factors (CCF).
- $D_i$: Discount factor based on Effective Interest Rate (EIR): $D_i = (1 + r)^{-t_i}$.

### Basel III Capital Adequacy Ratio (CAR)
Capital adequacy resilience is evaluated under standard standardized and internal rating-based (IRB) frameworks:

$$\text{CAR} = \frac{\text{Tier 1 Capital} + \text{Tier 2 Capital}}{\sum (\text{EAD}_i \times w_i) + \text{RWA}_{\text{Operational}} + \text{RWA}_{\text{Market}}}$$

Where $w_i$ denotes the regulatory risk weight assigned to obligor grade and collateral grade.

### Kolmogorov-Smirnov (KS) Statistic
To validate that the predictive model effectively separates good credits from defaulting accounts:

$$\text{KS} = \max_{s \in [0, 1]} \left| F_{\text{default}}(s) - F_{\text{performing}}(s) \right| = 49.05\%$$

---

## 5. Machine Learning & Predictive Risk Validation

The supervised credit intelligence pipeline trains a tuned Gradient Boosting Classifier with cross-validated hyper-parameters over customer credit profiles, balance sheets, and behavioral history.

<p align="center">
  <img src="assets/model_roc_curve.png" alt="AURA Model ROC Curve" width="48%" />
  <img src="assets/ifrs9_ecl_stage_breakdown.png" alt="IFRS 9 ECL Stage Breakdown" width="48%" />
</p>

### Feature Importance Distribution
1. **Debt-to-Income (DTI) Ratio** (Weight: 26.4%): Primary predictor of personal leverage and repayment vulnerability.
2. **Revolving Credit Utilization** (Weight: 22.8%): Early-warning indicator of liquidity strain.
3. **Internal Credit Score / Bureau FICO** (Weight: 19.5%): Historical repayment discipline baseline.
4. **Historical Delinquency (30/60/90 DPD)** (Weight: 14.1%): Direct trigger for Significant Increase in Credit Risk (SICR).
5. **Annual Income & Loan-to-Value (LTV)** (Weight: 17.2%): Collateral buffer and repayment capacity.

### Unsupervised AML Anomaly Engine
The Isolation Forest engine assesses real-time payment transactions on 4 core dimensional vectors:
- Normalized Transaction Amount relative to customer 30-day rolling baseline.
- Frequency and transaction velocity within 60-minute burst windows.
- High-risk destination flag (FATF grey/black listed jurisdictions).
- Structuring indicator (repeated amounts immediately beneath €10,000 regulatory reporting threshold).

---

## 6. Enterprise Power BI Suite & Kimball Data Model

The presentation tier is structured in a pure Kimball Star Schema optimized for Microsoft Power BI Desktop, Microsoft Fabric, and PBIP deployment.

```
       [dim_customers]            [dim_macro_stress]
              │                            │
              ▼                            ▼
      ┌──────────────────────────────────────────┐
      │       fact_credit_portfolio (10k)        │
      │ ──────────────────────────────────────── │
      │ loan_id (PK)      ead_exposure           │
      │ customer_id (FK)  pd_calibrated          │
      │ stage_id          lgd_percentage         │
      │ risk_weight       ifrs9_ecl_amount       │
      └──────────────────────────────────────────┘
                            │
                            ▼
      ┌──────────────────────────────────────────┐
      │      fact_transactions_stream (25k)      │
      │ ──────────────────────────────────────── │
      │ txn_id (PK)       aml_anomaly_score      │
      │ customer_id (FK)  is_aml_flagged         │
      │ txn_amount        timestamp              │
      └──────────────────────────────────────────┘
```

### Core Enterprise DAX Measures
Selected production DAX measures included in `powerbi/dax_enterprise_measure_library.dax`:

```dax
// 1. Total Portfolio Expected Credit Loss (IFRS 9)
[ECL_Total_EUR] = 
SUMX(
    fact_credit_portfolio,
    fact_credit_portfolio[ead_exposure] * 
    fact_credit_portfolio[pd_calibrated] * 
    fact_credit_portfolio[lgd_percentage]
)

// 2. Basel III Capital Adequacy Ratio (CAR %)
[Basel_III_CAR_Pct] = 
DIVIDE(
    [Tier_1_Capital_Base_EUR],
    [Total_RWA_EUR],
    0
)

// 3. Stressed CAR under Severely Adverse Macro Scenario
[Stressed_CAR_Severe_Pct] = 
VAR StressedECL = [ECL_Total_EUR] * (1 + SELECTEDVALUE(dim_macro_stress[gdp_shock_pct], 0.35))
VAR DepletedTier1 = [Tier_1_Capital_Base_EUR] - StressedECL
VAR StressedRWA = [Total_RWA_EUR] * 1.15
RETURN
DIVIDE(DepletedTier1, StressedRWA, 0)
```

---

## 7. Repository Structure

```
AURA-FinTech-Risk-Intelligence/
├── assets/
│   ├── powerbi_executive_boardroom_cockpit.png  # Ultra-HD Boardroom preview
│   ├── model_roc_curve.png                      # Validation ROC Curve (AUC 0.8142)
│   └── ifrs9_ecl_stage_breakdown.png            # Staging allocation charts
├── data/
│   ├── aura_fintech.duckdb                      # High-speed analytical DB with Medallion dbt models
│   ├── fact_credit_portfolio.csv                # 10,000 corporate & retail loan facilities
│   ├── fact_transactions_stream.csv             # 25,000 payment records with AML features
│   ├── dim_macro_stress_scenarios.csv           # Baseline, Mild, and Severely Adverse shocks
│   ├── fct_ifrs9_ecl_provisions.csv             # dbt Gold: IFRS 9 ECL staged provisions
│   ├── fct_basel_iii_capital_adequacy.csv       # dbt Gold: Basel III CAR & RWA structure
│   ├── fct_macro_stress_testing_impact.csv      # dbt Gold: Multi-scenario capital depletion
│   ├── fct_aml_forensic_watchlist.csv           # dbt Gold: Prioritized AML surveillance list
│   └── fct_portfolio_country_risk.csv           # dbt Gold: Sovereign credit distribution
├── dbt_project.yml                              # Enterprise dbt project configuration
├── profiles.yml                                 # dbt DuckDB adapter connection profile
├── macros/
│   ├── calculate_ecl.sql                        # dbt macro: IFRS 9 discounted Expected Credit Loss
│   └── classify_aml_risk.sql                    # dbt macro: Multi-factor transaction risk rule
├── models/
│   ├── 1_bronze/                                # Raw Ingestion & Schema Enforcement Layer
│   │   ├── src_fintech.yml                      # Source declarations & schema integrity tests
│   │   ├── stg_credit_portfolio.sql             # Staged loan exposures and delinquency
│   │   ├── stg_transactions_stream.sql          # Staged real-time payment transactions
│   │   └── stg_macro_scenarios.sql              # Staged Basel III macro stress shocks
│   ├── 2_silver/                                # Feature Engineering & Cleansed Core
│   │   ├── int_credit_risk_staging.sql          # SICR triggers, DTI bands, and Basel weights
│   │   └── int_aml_behavioral_metrics.sql       # Rolling window velocity, Z-scores & smurfing
│   └── 3_gold/                                  # Executive Dimensional Marts
│       ├── fct_ifrs9_ecl_provisions.sql         # Stage 1-3 ECL allowances & coverage
│       ├── fct_basel_iii_capital_adequacy.sql   # CAR 14.50%, Tier 1 capital & buffer surplus
│       ├── fct_macro_stress_testing_impact.sql  # Macro stress depletion (Severely Adverse)
│       ├── fct_aml_forensic_watchlist.sql       # Forensic AML suspect accounts & SAR filing
│       └── fct_portfolio_country_risk.sql       # European sovereign market credit concentration
├── sql/                                         # Advanced SQL Analytics Suite
│   ├── 01_ifrs9_credit_migration_matrix.sql     # Multi-period Markov rating transition matrix
│   ├── 02_aml_transaction_structuring_detector.sql # Rolling lag/lead smurfing threshold detector
│   ├── 03_basel_iii_pillar1_capital_optimization.sql # Standardized vs IRB capital relief model
│   ├── 04_macro_stress_scenario_sensitivity.sql # Dynamic sensitivity grid under GDP/Rate shocks
│   └── 05_vintage_loss_curve_analysis.sql       # Multi-cohort loan vintage survival curves
├── powerbi/
│   ├── AURA_FinTech_Enterprise_Cockpit.pbix     # Full-featured Power BI Desktop Report
│   ├── AURA_FinTech_DataModel_Gold_Enterprise.xlsx # Multi-tab Gold dimensional model
│   ├── AURA_FinTech_Risk.pbip                   # Microsoft Fabric / PBIP developer project
│   ├── aura_fintech_powerbi_report_schema.json  # 4-page Fabric PBIP report metadata
│   └── dax_enterprise_measure_library.dax       # 18 production DAX risk calculations
├── models/                                      # ML Trained Weights & Pipelines
│   ├── credit_default_gb_model.joblib           # Gradient Boosting Classifier (ROC-AUC 0.8142)
│   └── aml_isolation_forest.joblib              # Unsupervised Isolation Forest Anomaly Model
├── generate_fintech_dataset.py                  # Synthetic data generator engine
├── train_risk_models.py                         # ML training, validation, and chart generation
├── requirements.txt                             # Python dependencies (dbt, duckdb, sklearn)
├── .gitignore                                   # Standard repo ignore rules
├── LICENSE                                      # MIT Open Source License
└── README.md                                    # Comprehensive whitepaper & documentation
```

---

## 8. Quickstart & Reproducibility Guide

### Step 1: Clone the Repository
```bash
git clone https://github.com/debbrataadhikary/AURA-FinTech-Risk-Intelligence.git
cd AURA-FinTech-Risk-Intelligence
```

### Step 2: Set Up Environment & Install Dependencies
```bash
python -m venv venv
venv\Scripts\activate       # On Linux/macOS: source venv/bin/activate
pip install -r requirements.txt
pip install dbt-duckdb
```

### Step 3: Run the Complete dbt Medallion Pipeline
```bash
dbt run --profiles-dir .
dbt test --profiles-dir .
```
*Executes all 10 Bronze, Silver, and Gold SQL models and validates 4 data tests in < 1 second.*

### Step 4: Run Advanced SQL Analytics
```bash
python -c "
import duckdb
con = duckdb.connect('data/aura_fintech.duckdb', read_only=True)
print(con.execute(open('sql/01_ifrs9_credit_migration_matrix.sql').read()).df())
"
```

### Step 5: Launch Power BI Desktop
Double-click `powerbi/AURA_FinTech_Enterprise_Cockpit.pbix` to explore the interactive visual cockpit, or connect Power BI Desktop to `powerbi/AURA_FinTech_DataModel_Gold_Enterprise.xlsx`.


---

## 9. Author & Professional Portfolio

**Debbrata Adhikary**  
*Lead Data Architect & Senior Analytics Engineer*  
- **GitHub**: [github.com/debbrataadhikary](https://github.com/debbrataadhikary)  
- **LinkedIn**: [linkedin.com/in/debbrataadhikary](https://linkedin.com/in/debbrataadhikary)  
- **Specializations**: Enterprise Power BI, Financial Risk Modeling, DuckDB / Lakehouse Engineering, Regulatory Reporting (Basel III, IFRS 9).

---

## 10. License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
