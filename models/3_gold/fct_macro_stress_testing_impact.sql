{{ config(materialized='table') }}

WITH base_capital AS (
    SELECT * FROM {{ ref('fct_basel_iii_capital_adequacy') }}
),

macro_scenarios AS (
    SELECT * FROM {{ ref('stg_macro_scenarios') }}
)

SELECT
    m.scenario_name,
    m.gdp_growth_pct,
    m.inflation_hicp_pct,
    m.central_bank_rate_pct,
    m.unemployment_pct,
    m.ecl_stress_multiplier,

    c.total_portfolio_ead_eur,
    c.total_rwa_eur AS baseline_rwa_eur,
    c.tier1_capital_eur AS baseline_tier1_eur,
    c.capital_adequacy_ratio_car_pct AS baseline_car_pct,

    -- Stressed Credit Impairment Provision
    ROUND(c.total_rwa_eur * 0.038 * m.ecl_stress_multiplier, 2) AS stressed_ecl_provision_eur,

    -- Depleted Tier 1 Capital under Stress
    ROUND(c.tier1_capital_eur - (c.total_rwa_eur * 0.038 * (m.ecl_stress_multiplier - 1.0)), 2) AS stressed_tier1_capital_eur,

    -- Stressed RWA (Asset Inflation from rating migration)
    ROUND(c.total_rwa_eur * (1.0 + (m.ecl_stress_multiplier - 1.0) * 0.15), 2) AS stressed_rwa_eur,

    -- Stressed CAR Ratio (%)
    ROUND(
        ((c.tier1_capital_eur - (c.total_rwa_eur * 0.038 * (m.ecl_stress_multiplier - 1.0))) / 
         (c.total_rwa_eur * (1.0 + (m.ecl_stress_multiplier - 1.0) * 0.15))) * 100, 2
    ) AS stressed_car_ratio_pct,

    -- Solvency Buffer Depletion (bps)
    ROUND(
        (c.capital_adequacy_ratio_car_pct - 
         (((c.tier1_capital_eur - (c.total_rwa_eur * 0.038 * (m.ecl_stress_multiplier - 1.0))) / 
           (c.total_rwa_eur * (1.0 + (m.ecl_stress_multiplier - 1.0) * 0.15))) * 100)) * 100, 0
    ) AS solvency_depletion_bps

FROM base_capital c
CROSS JOIN macro_scenarios m
ORDER BY m.ecl_stress_multiplier ASC
