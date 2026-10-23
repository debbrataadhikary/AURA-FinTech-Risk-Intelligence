{{ config(materialized='table') }}

WITH silver_loans AS (
    SELECT * FROM {{ ref('int_credit_risk_staging') }}
)

SELECT
    country AS sovereign_market,
    COUNT(loan_id) AS total_active_loans,
    ROUND(SUM(ead_exposure_eur), 2) AS total_ead_eur,
    ROUND(AVG(fico_score), 0) AS avg_fico_credit_score,
    ROUND(AVG(debt_to_income_dti) * 100, 2) AS avg_dti_ratio_pct,
    ROUND(AVG(pd_probability_of_default) * 100, 2) AS avg_default_probability_pct,
    ROUND(SUM(dynamic_ecl_eur), 2) AS total_ecl_eur,
    ROUND((SUM(dynamic_ecl_eur) / NULLIF(SUM(ead_exposure_eur), 0)) * 100, 2) AS impairment_density_pct,
    ROUND(SUM(CASE WHEN days_past_due_dpd >= 90 THEN ead_exposure_eur ELSE 0 END), 2) AS npl_non_performing_loans_eur,
    ROUND((SUM(CASE WHEN days_past_due_dpd >= 90 THEN ead_exposure_eur ELSE 0 END) / NULLIF(SUM(ead_exposure_eur), 0)) * 100, 2) AS npl_ratio_pct
FROM silver_loans
GROUP BY country
ORDER BY total_ead_eur DESC
