-- ==============================================================================
-- SCRIPT 04: Macroeconomic Stress Testing Dynamic Sensitivity Matrix
-- OBJECTIVE: Multi-scenario sensitivity of Capital Buffers under EBA / ECB shocks
-- TECHNIQUES: Cross-Cartesian Factor Multipliers, Loss Depletion Analytics
-- ==============================================================================

WITH base_book AS (
    SELECT
        COUNT(loan_id) AS total_loans,
        SUM(ead_exposure_eur) AS total_ead,
        SUM(dynamic_ecl_eur) AS baseline_ecl,
        SUM(rwa_amount_eur) AS baseline_rwa,
        SUM(rwa_amount_eur) * 0.1450 AS baseline_tier1_capital
    FROM int_credit_risk_staging
),

macro_grid AS (
    SELECT * FROM stg_macro_scenarios
)

SELECT
    m.scenario_name,
    m.gdp_growth_pct,
    m.inflation_hicp_pct,
    m.central_bank_rate_pct,
    m.unemployment_pct,
    m.ecl_stress_multiplier,
    
    ROUND(b.baseline_ecl, 2) AS baseline_ecl_eur,
    ROUND(b.baseline_ecl * m.ecl_stress_multiplier, 2) AS stressed_ecl_eur,
    ROUND((b.baseline_ecl * (m.ecl_stress_multiplier - 1.0)), 2) AS incremental_ecl_loss_eur,
    
    ROUND(b.baseline_tier1_capital, 2) AS baseline_tier1_eur,
    ROUND(b.baseline_tier1_capital - (b.baseline_ecl * (m.ecl_stress_multiplier - 1.0)), 2) AS post_stress_tier1_capital_eur,
    
    ROUND((b.baseline_tier1_capital / b.baseline_rwa) * 100, 2) AS baseline_tier1_ratio_pct,
    ROUND(
        ((b.baseline_tier1_capital - (b.baseline_ecl * (m.ecl_stress_multiplier - 1.0))) / 
         (b.baseline_rwa * (1.0 + (m.ecl_stress_multiplier - 1.0) * 0.12))) * 100, 2
    ) AS post_stress_tier1_ratio_pct,
    
    CASE 
        WHEN ((b.baseline_tier1_capital - (b.baseline_ecl * (m.ecl_stress_multiplier - 1.0))) / 
              (b.baseline_rwa * (1.0 + (m.ecl_stress_multiplier - 1.0) * 0.12))) * 100 >= 10.50 
        THEN 'ADEQUATE_CAPITAL_SURPLUS'
        ELSE 'CAPITAL_BREACH_RESTRICTION'
    END AS regulatory_solvency_verdict

FROM base_book b
CROSS JOIN macro_grid m
ORDER BY m.ecl_stress_multiplier ASC;
