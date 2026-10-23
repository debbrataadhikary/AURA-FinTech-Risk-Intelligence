{{ config(materialized='table') }}

WITH silver_portfolio AS (
    SELECT * FROM {{ ref('int_credit_risk_staging') }}
),

portfolio_aggregates AS (
    SELECT
        COUNT(loan_id) AS total_obligors_count,
        SUM(ead_exposure_eur) AS total_exposure_at_default_eur,
        SUM(rwa_amount_eur) AS total_rwa_eur,
        SUM(dynamic_ecl_eur) AS total_impairment_provisions_eur
    FROM silver_portfolio
),

capital_structure AS (
    SELECT
        total_obligors_count,
        total_exposure_at_default_eur,
        total_rwa_eur,
        total_impairment_provisions_eur,

        -- Institutional Capital Base
        ROUND(total_rwa_eur * 0.1450, 2) AS tier1_capital_eur,
        ROUND(total_rwa_eur * 0.0250, 2) AS tier2_capital_eur
    FROM portfolio_aggregates
)

SELECT
    total_obligors_count,
    ROUND(total_exposure_at_default_eur, 2) AS total_portfolio_ead_eur,
    ROUND(total_rwa_eur, 2) AS total_rwa_eur,
    tier1_capital_eur,
    tier2_capital_eur,
    ROUND(tier1_capital_eur + tier2_capital_eur, 2) AS total_regulatory_capital_eur,

    -- Capital Adequacy Ratio (CAR %)
    ROUND(((tier1_capital_eur + tier2_capital_eur) / total_rwa_eur) * 100, 2) AS capital_adequacy_ratio_car_pct,

    -- Tier 1 Capital Ratio (%)
    ROUND((tier1_capital_eur / total_rwa_eur) * 100, 2) AS tier1_capital_ratio_pct,

    -- Statutory Minimum with Conservation Buffer (10.50%)
    10.50 AS statutory_minimum_car_pct,

    -- Capital Surplus / Buffer over Regulatory Floor (bps)
    ROUND((((tier1_capital_eur + tier2_capital_eur) / total_rwa_eur) * 100 - 10.50) * 100, 0) AS capital_buffer_surplus_bps

FROM capital_structure
