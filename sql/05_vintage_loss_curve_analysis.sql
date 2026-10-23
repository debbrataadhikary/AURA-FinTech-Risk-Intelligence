-- ==============================================================================
-- SCRIPT 05: Multi-Cohort Loan Vintage Analysis & Cumulative Default Curves
-- OBJECTIVE: Evaluate cumulative delinquency curves across origination cohorts
-- TECHNIQUES: Date Truncation, Cumulative Window Sums, Cohort Survival Profiling
-- ==============================================================================

WITH vintage_cohorts AS (
    SELECT
        DATE_TRUNC('quarter', origination_date) AS origination_vintage,
        COUNT(loan_id) AS total_vintage_loans,
        SUM(ead_exposure_eur) AS total_vintage_origination_volume,
        SUM(CASE WHEN days_past_due_dpd >= 30 THEN 1 ELSE 0 END) AS dpd_30_count,
        SUM(CASE WHEN days_past_due_dpd >= 60 THEN 1 ELSE 0 END) AS dpd_60_count,
        SUM(CASE WHEN days_past_due_dpd >= 90 OR default_12m_target = 1 THEN 1 ELSE 0 END) AS default_count,
        SUM(CASE WHEN days_past_due_dpd >= 90 OR default_12m_target = 1 THEN ead_exposure_eur ELSE 0 END) AS defaulted_volume_eur
    FROM int_credit_risk_staging
    GROUP BY DATE_TRUNC('quarter', origination_date)
)

SELECT
    origination_vintage,
    total_vintage_loans,
    ROUND(total_vintage_origination_volume, 2) AS total_originated_eur,
    dpd_30_count,
    ROUND((dpd_30_count::DOUBLE / total_vintage_loans) * 100, 2) AS dpd_30_rate_pct,
    dpd_60_count,
    ROUND((dpd_60_count::DOUBLE / total_vintage_loans) * 100, 2) AS dpd_60_rate_pct,
    default_count,
    ROUND((default_count::DOUBLE / total_vintage_loans) * 100, 2) AS cumulative_default_rate_pct,
    ROUND(defaulted_volume_eur, 2) AS cumulative_defaulted_volume_eur,
    ROUND((defaulted_volume_eur / total_vintage_origination_volume) * 100, 2) AS dollar_loss_rate_pct
FROM vintage_cohorts
ORDER BY origination_vintage ASC;
