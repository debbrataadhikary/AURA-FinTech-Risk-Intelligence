{{ config(materialized='table') }}

WITH staged AS (
    SELECT * FROM {{ ref('stg_credit_portfolio') }}
),

engineered AS (
    SELECT
        loan_id,
        customer_id,
        borrower_age,
        annual_income_eur,
        fico_score,
        debt_to_income_dti,
        employment_length_years,
        loan_amount_eur,
        loan_purpose,
        term_months,
        interest_rate_pct,
        days_past_due_dpd,
        ead_exposure_eur,
        lgd_loss_given_default,
        pd_probability_of_default,
        default_12m_target,
        origination_date,
        country,

        -- Credit Quality Band
        CASE
            WHEN fico_score >= 720 THEN 'PRIME'
            WHEN fico_score >= 660 THEN 'NEAR_PRIME'
            ELSE 'SUBPRIME'
        END AS credit_quality_band,

        -- Leverage Bucket
        CASE
            WHEN debt_to_income_dti < 0.30 THEN 'LOW_LEVERAGE'
            WHEN debt_to_income_dti <= 0.45 THEN 'MODERATE_LEVERAGE'
            ELSE 'HIGH_LEVERAGE_STRESSED'
        END AS leverage_bucket,

        -- Delinquency Severity
        CASE
            WHEN days_past_due_dpd = 0 THEN 'CURRENT_PERFORMING'
            WHEN days_past_due_dpd <= 30 THEN 'EARLY_DELINQUENT_1_30'
            WHEN days_past_due_dpd <= 60 THEN 'MID_DELINQUENT_31_60'
            WHEN days_past_due_dpd <= 90 THEN 'SERIOUS_DELINQUENT_61_90'
            ELSE 'DEFAULT_OVER_90'
        END AS delinquency_status,

        -- Significant Increase in Credit Risk (SICR) Trigger under IFRS 9
        CASE
            WHEN days_past_due_dpd >= 30 
                 OR pd_probability_of_default >= 0.080 
                 OR (debt_to_income_dti > 0.45 AND fico_score < 650)
            THEN 1 
            ELSE 0 
        END AS is_sicr_triggered,

        -- Basel III Standardized Risk Weighting (%)
        CASE
            WHEN days_past_due_dpd >= 90 OR default_12m_target = 1 THEN 1.50
            WHEN fico_score < 660 OR debt_to_income_dti > 0.45 THEN 1.00
            WHEN fico_score < 720 THEN 0.75
            ELSE 0.35
        END AS basel_risk_weight_multiplier

    FROM staged
),

classified AS (
    SELECT
        *,
        -- IFRS 9 Multi-Stage Regulatory Allocation
        CASE
            WHEN days_past_due_dpd >= 90 OR default_12m_target = 1 THEN 'Stage 3 (Credit-Impaired)'
            WHEN is_sicr_triggered = 1 THEN 'Stage 2 (Significant Risk Surge)'
            ELSE 'Stage 1 (Performing 12M)'
        END AS ifrs9_stage_assigned,

        -- Basel III Risk-Weighted Asset (RWA)
        (ead_exposure_eur * basel_risk_weight_multiplier) AS rwa_amount_eur,

        -- Minimum Pillar 1 Capital Requirement (8% of RWA)
        (ead_exposure_eur * basel_risk_weight_multiplier * 0.08) AS pillar1_capital_required_eur,

        -- Dynamic IFRS 9 Expected Credit Loss (Discounted Cash Flow)
        {{ calculate_ecl('ead_exposure_eur', 'pd_probability_of_default', 'lgd_loss_given_default', 0.035, 'term_months / 12.0') }} AS dynamic_ecl_eur

    FROM engineered
)

SELECT * FROM classified
