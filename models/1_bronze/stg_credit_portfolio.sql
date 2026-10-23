{{ config(materialized='view') }}

WITH raw_source AS (
    SELECT * FROM {{ source('aura_raw', 'fact_credit_portfolio') }}
)

SELECT
    CAST(loan_id AS VARCHAR) AS loan_id,
    CAST(customer_id AS VARCHAR) AS customer_id,
    CAST(age AS INTEGER) AS borrower_age,
    CAST(annual_income_eur AS DOUBLE) AS annual_income_eur,
    CAST(fico_score AS INTEGER) AS fico_score,
    CAST(debt_to_income_dti AS DOUBLE) AS debt_to_income_dti,
    CAST(employment_length_years AS INTEGER) AS employment_length_years,
    CAST(loan_amount_eur AS DOUBLE) AS loan_amount_eur,
    CAST(loan_purpose AS VARCHAR) AS loan_purpose,
    CAST(term_months AS INTEGER) AS term_months,
    CAST(interest_rate_pct AS DOUBLE) AS interest_rate_pct,
    CAST(days_past_due_dpd AS INTEGER) AS days_past_due_dpd,
    CAST(ifrs9_stage AS VARCHAR) AS ifrs9_stage_raw,
    CAST(ead_exposure_eur AS DOUBLE) AS ead_exposure_eur,
    CAST(lgd_loss_given_default AS DOUBLE) AS lgd_loss_given_default,
    CAST(pd_probability_of_default AS DOUBLE) AS pd_probability_of_default,
    CAST(ecl_expected_loss_eur AS DOUBLE) AS ecl_expected_loss_eur,
    CAST(default_12m_target AS INTEGER) AS default_12m_target,
    CAST(origination_date AS DATE) AS origination_date,
    CAST(country AS VARCHAR) AS country
FROM raw_source
WHERE loan_id IS NOT NULL
