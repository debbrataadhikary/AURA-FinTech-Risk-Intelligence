-- ==============================================================================
-- SCRIPT 01: IFRS 9 Multi-Period Credit Rating Migration & Transition Matrix
-- OBJECTIVE: Quantify obligor credit grade degradation/upgrade probabilities
-- TECHNIQUES: Recursive CTEs, Window Aggregations, Conditional Transition Matrices
-- ==============================================================================

WITH cohort_base AS (
    SELECT
        loan_id,
        customer_id,
        origination_date,
        term_months,
        credit_quality_band AS initial_rating,
        delinquency_status,
        ifrs9_stage_assigned AS current_stage,
        ead_exposure_eur,
        pd_probability_of_default
    FROM int_credit_risk_staging
),

rating_transitions AS (
    SELECT
        initial_rating,
        current_stage,
        COUNT(loan_id) AS transition_count,
        SUM(ead_exposure_eur) AS transition_ead_volume_eur,
        ROUND(AVG(pd_probability_of_default) * 100, 2) AS avg_migration_pd_pct
    FROM cohort_base
    GROUP BY initial_rating, current_stage
),

marginal_totals AS (
    SELECT
        initial_rating,
        SUM(transition_count) AS total_initial_obligors,
        SUM(transition_ead_volume_eur) AS total_initial_ead_volume
    FROM rating_transitions
    GROUP BY initial_rating
)

SELECT
    t.initial_rating AS origination_rating_grade,
    t.current_stage AS current_regulatory_stage,
    t.transition_count,
    m.total_initial_obligors,
    ROUND((t.transition_count::DOUBLE / m.total_initial_obligors) * 100, 2) AS transition_probability_pct,
    t.transition_ead_volume_eur,
    ROUND((t.transition_ead_volume_eur / m.total_initial_ead_volume) * 100, 2) AS ead_migration_share_pct,
    t.avg_migration_pd_pct
FROM rating_transitions t
INNER JOIN marginal_totals m ON t.initial_rating = m.initial_rating
ORDER BY t.initial_rating, t.current_stage;
