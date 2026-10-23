# -*- coding: utf-8 -*-
"""
generate_fintech_dataset.py
AURA-FinTech: Autonomous Risk Architecture & Credit Intelligence
----------------------------------------------------------------
Generates an enterprise-grade synthetic dataset of:
1. Loans & Credit Portfolio (IFRS 9 3-Stage Classification: Performing, Underperforming, Default)
2. Transactions Stream (SEPA, SWIFT, Card with AML / Mule indicators)
3. Macroeconomic Scenarios (Base, Stagnation, Severe Recession)
"""

import os
import duckdb
import numpy as np
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

np.random.seed(42)

def generate_credit_portfolio(n_loans=10000):
    print(f"Generating {n_loans} credit portfolio records...")
    customer_ids = [f"CUST-{100000 + i}" for i in range(n_loans)]
    loan_ids = [f"LN-2026-{200000 + i}" for i in range(n_loans)]
    
    # Customer Demographics & Credit Scores
    ages = np.random.randint(21, 68, n_loans)
    annual_income = np.round(np.random.lognormal(mean=10.6, sigma=0.55, size=n_loans), 2) # median ~40k EUR
    fico_scores = np.clip(np.random.normal(loc=680, scale=85, size=n_loans).astype(int), 320, 850)
    debt_to_income = np.round(np.clip(np.random.beta(a=2, b=5, size=n_loans) * 0.85, 0.05, 0.75), 3)
    employment_length = np.random.randint(0, 25, n_loans)
    
    # Loan Attributes
    loan_amounts = np.round(np.random.choice([5000, 10000, 15000, 25000, 45000, 75000, 150000], size=n_loans, p=[0.25, 0.25, 0.20, 0.15, 0.08, 0.05, 0.02]), 2)
    loan_purpose = np.random.choice(["Home Improvement", "Debt Consolidation", "SME Working Capital", "Green Energy Transition", "Vehicle Purchase"], size=n_loans)
    loan_term_months = np.random.choice([12, 24, 36, 48, 60, 84], size=n_loans, p=[0.1, 0.2, 0.35, 0.15, 0.15, 0.05])
    interest_rate = np.round(np.clip(14.5 - (fico_scores - 350) * 0.018 + debt_to_income * 6.5, 3.25, 24.50), 2)
    
    # Repayment Performance & Delinquency
    days_past_due = np.zeros(n_loans, dtype=int)
    # create delinquency distribution
    delinq_mask = np.random.rand(n_loans) < (0.28 - (fico_scores / 3200))
    days_past_due[delinq_mask] = np.random.choice([15, 35, 65, 95, 120, 180], size=np.sum(delinq_mask), p=[0.45, 0.25, 0.15, 0.08, 0.04, 0.03])
    
    # IFRS 9 Stage Determination
    # Stage 1: Performing (DPD <= 30), Stage 2: Underperforming / Significant Increase in Credit Risk (30 < DPD <= 90), Stage 3: Credit Impaired / Default (DPD > 90)
    ifrs9_stage = np.where(days_past_due <= 30, "Stage 1 (Performing)",
                  np.where(days_past_due <= 90, "Stage 2 (SICR - Underperforming)", "Stage 3 (Default - Credit Impaired)"))
    
    # Target Variable: Default within 12M (binary)
    # Logit formula based on FICO, DTI, DPD, Income
    z = -3.8 - 0.009 * (fico_scores - 650) + 4.2 * debt_to_income + 0.045 * days_past_due - 0.000015 * annual_income
    prob_default = 1 / (1 + np.exp(-z))
    default_flag = (np.random.rand(n_loans) < prob_default).astype(int)
    # Ensure all Stage 3 are marked default
    default_flag[days_past_due > 90] = 1
    
    # Exposure at Default (EAD) & Loss Given Default (LGD)
    ead_eur = np.round(loan_amounts * np.random.uniform(0.65, 0.98, n_loans), 2)
    lgd_rate = np.round(np.clip(np.random.normal(0.45, 0.12, n_loans), 0.15, 0.85), 3) # Basel benchmark ~45%
    ecl_expected_loss = np.round(prob_default * ead_eur * lgd_rate, 2)
    
    df_loans = pd.DataFrame({
        "Loan_ID": loan_ids,
        "Customer_ID": customer_ids,
        "Age": ages,
        "Annual_Income_EUR": annual_income,
        "FICO_Score": fico_scores,
        "Debt_to_Income_DTI": debt_to_income,
        "Employment_Length_Years": employment_length,
        "Loan_Amount_EUR": loan_amounts,
        "Loan_Purpose": loan_purpose,
        "Term_Months": loan_term_months,
        "Interest_Rate_Pct": interest_rate,
        "Days_Past_Due_DPD": days_past_due,
        "IFRS9_Stage": ifrs9_stage,
        "EAD_Exposure_EUR": ead_eur,
        "LGD_Loss_Given_Default": lgd_rate,
        "PD_Probability_of_Default": np.round(prob_default, 4),
        "ECL_Expected_Loss_EUR": ecl_expected_loss,
        "Default_12M_Target": default_flag,
        "Origination_Date": pd.date_range(start="2024-01-01", periods=n_loans, freq="40min").strftime("%Y-%m-%d"),
        "Country": np.random.choice(["Lithuania", "Germany", "Estonia", "Netherlands", "Latvia"], size=n_loans, p=[0.35, 0.25, 0.15, 0.15, 0.10])
    })
    
    loans_path = os.path.join(DATA_DIR, "fact_credit_portfolio.csv")
    df_loans.to_csv(loans_path, index=False)
    print(f"Credit Portfolio saved: {loans_path} (Shape: {df_loans.shape})")
    return df_loans


def generate_transactions_stream(n_tx=25000):
    print(f"Generating {n_tx} transaction streaming records...")
    tx_ids = [f"TXN-{1000000 + i}" for i in range(n_tx)]
    customer_ids = [f"CUST-{100000 + np.random.randint(0, 10000)}" for _ in range(n_tx)]
    
    channels = np.random.choice(["SEPA Instant", "SWIFT Wire", "POS Card", "ATM Withdrawal", "P2P Mobile"], size=n_tx, p=[0.40, 0.10, 0.30, 0.08, 0.12])
    amounts = np.round(np.where(channels == "SWIFT Wire", np.random.exponential(12000, n_tx),
                       np.where(channels == "SEPA Instant", np.random.exponential(850, n_tx),
                                np.random.exponential(65, n_tx))), 2)
    amounts = np.clip(amounts, 1.50, 450000.0)
    
    # AML & Velocity Flags
    is_foreign_counterparty = np.random.choice([0, 1], size=n_tx, p=[0.82, 0.18])
    is_high_risk_jurisdiction = np.random.choice([0, 1], size=n_tx, p=[0.96, 0.04])
    tx_velocity_1h = np.random.poisson(lam=1.8, size=n_tx)
    
    # Anomaly / Mule Scoring
    fraud_prob = (
        0.005 
        + 0.04 * (amounts > 10000) 
        + 0.08 * is_high_risk_jurisdiction 
        + 0.05 * (tx_velocity_1h > 5)
    )
    is_suspicious_aml = (np.random.rand(n_tx) < fraud_prob).astype(int)
    
    df_tx = pd.DataFrame({
        "Transaction_ID": tx_ids,
        "Customer_ID": customer_ids,
        "Channel": channels,
        "Amount_EUR": amounts,
        "Is_Foreign_Counterparty": is_foreign_counterparty,
        "Is_High_Risk_Jurisdiction": is_high_risk_jurisdiction,
        "Hourly_Velocity_Count": tx_velocity_1h,
        "AML_Suspicious_Flag": is_suspicious_aml,
        "Timestamp": pd.date_range(start="2026-09-01", periods=n_tx, freq="2min").strftime("%Y-%m-%d %H:%M:%S")
    })
    
    tx_path = os.path.join(DATA_DIR, "fact_transactions_stream.csv")
    df_tx.to_csv(tx_path, index=False)
    print(f"Transactions Stream saved: {tx_path} (Shape: {df_tx.shape})")
    return df_tx


def generate_macro_scenarios():
    print("Generating Basel III / IFRS 9 Macroeconomic Stress Scenarios...")
    scenarios = [
        {"Scenario": "Baseline (ECB Projections)", "GDP_Growth_Pct": 1.4, "Inflation_HICP_Pct": 2.2, "Central_Bank_Rate_Pct": 3.25, "Unemployment_Pct": 6.4, "ECL_Stress_Multiplier": 1.00},
        {"Scenario": "Stagnation (Adverse Stagflation)", "GDP_Growth_Pct": -0.4, "Inflation_HICP_Pct": 4.8, "Central_Bank_Rate_Pct": 4.50, "Unemployment_Pct": 8.2, "ECL_Stress_Multiplier": 1.45},
        {"Scenario": "Severe Recession (Global Liquidity Shock)", "GDP_Growth_Pct": -2.8, "Inflation_HICP_Pct": 6.5, "Central_Bank_Rate_Pct": 5.25, "Unemployment_Pct": 11.0, "ECL_Stress_Multiplier": 2.15}
    ]
    df_sc = pd.DataFrame(scenarios)
    sc_path = os.path.join(DATA_DIR, "dim_macro_stress_scenarios.csv")
    df_sc.to_csv(sc_path, index=False)
    print(f"Macro Scenarios saved: {sc_path}")
    return df_sc


def initialize_duckdb_warehouse():
    print("Initializing embedded DuckDB high-performance analytical warehouse...")
    db_path = os.path.join(DATA_DIR, "aura_fintech.duckdb")
    con = duckdb.connect(db_path)
    
    loans_csv = os.path.join(DATA_DIR, "fact_credit_portfolio.csv").replace("\\", "/")
    tx_csv = os.path.join(DATA_DIR, "fact_transactions_stream.csv").replace("\\", "/")
    sc_csv = os.path.join(DATA_DIR, "dim_macro_stress_scenarios.csv").replace("\\", "/")
    
    con.execute(f"CREATE OR REPLACE TABLE fact_credit_portfolio AS SELECT * FROM read_csv_auto('{loans_csv}');")
    con.execute(f"CREATE OR REPLACE TABLE fact_transactions_stream AS SELECT * FROM read_csv_auto('{tx_csv}');")
    con.execute(f"CREATE OR REPLACE TABLE dim_macro_stress_scenarios AS SELECT * FROM read_csv_auto('{sc_csv}');")
    
    # Create Medallion Views: Gold Portfolio Summary
    con.execute("""
    CREATE OR REPLACE VIEW gold_ifrs9_stage_summary AS
    SELECT 
        IFRS9_Stage,
        Country,
        COUNT(*) AS Total_Loans,
        ROUND(SUM(EAD_Exposure_EUR), 2) AS Total_Exposure_EUR,
        ROUND(SUM(ECL_Expected_Loss_EUR), 2) AS Total_ECL_EUR,
        ROUND(AVG(PD_Probability_of_Default) * 100, 2) AS Avg_PD_Pct,
        ROUND(AVG(LGD_Loss_Given_Default) * 100, 2) AS Avg_LGD_Pct,
        ROUND(SUM(ECL_Expected_Loss_EUR) / SUM(EAD_Exposure_EUR) * 100, 2) AS ECL_Coverage_Ratio_Pct
    FROM fact_credit_portfolio
    GROUP BY IFRS9_Stage, Country;
    """)
    
    res = con.execute("SELECT IFRS9_Stage, SUM(Total_Loans) AS Loans, ROUND(SUM(Total_Exposure_EUR)/1e6, 2) AS Exposure_EUR_M FROM gold_ifrs9_stage_summary GROUP BY IFRS9_Stage;").fetchall()
    print("DuckDB Warehouse Stage Distribution:")
    for row in res:
        print(f"  -> {row[0]}: {row[1]} loans, EUR {row[2]}M Exposure")
    con.close()
    print(f"DuckDB database ready at: {db_path}")


if __name__ == "__main__":
    generate_credit_portfolio()
    generate_transactions_stream()
    generate_macro_scenarios()
    initialize_duckdb_warehouse()
