{{ config(materialized='table') }}

WITH silver_loans AS (
    SELECT * FROM {{ ref('int_credit_risk_staging') }}
)

SELECT
    ifrs9_stage_assigned,
    COUNT(loan_id) AS total_facilities_count,
    ROUND(SUM(ead_exposure_eur), 2) AS total_ead_exposure_eur,
    ROUND(AVG(pd_probability_of_default) * 100, 2) AS weighted_avg_pd_pct,
    ROUND(AVG(lgd_loss_given_default) * 100, 2) AS weighted_avg_lgd_pct,
    ROUND(SUM(dynamic_ecl_eur), 2) AS total_ecl_provision_eur,
    ROUND((SUM(dynamic_ecl_eur) / NULLIF(SUM(ead_exposure_eur), 0)) * 100, 2) AS ecl_coverage_ratio_pct,
    ROUND(SUM(rwa_amount_eur), 2) AS total_rwa_eur,
    ROUND(SUM(pillar1_capital_required_eur), 2) AS total_pillar1_capital_eur
FROM silver_loans
GROUP BY ifrs9_stage_assigned
ORDER BY total_ecl_provision_eur DESC
