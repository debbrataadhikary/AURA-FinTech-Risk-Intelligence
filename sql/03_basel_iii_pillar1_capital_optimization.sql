-- ==============================================================================
-- SCRIPT 03: Basel III Pillar 1 Capital Optimization & IRB Relief Analysis
-- OBJECTIVE: Model capital relief shifting from Standardized Approach (SA) to F-IRB
-- TECHNIQUES: Mathematical Risk-Weight Asset Formulas, Capital Optimization Modeling
-- ==============================================================================

WITH standardized_vs_irb AS (
    SELECT
        loan_id,
        customer_id,
        ead_exposure_eur,
        pd_probability_of_default,
        lgd_loss_given_default,
        basel_risk_weight_multiplier AS sa_risk_weight,
        
        -- Standardized Approach RWA
        (ead_exposure_eur * basel_risk_weight_multiplier) AS sa_rwa_eur,

        -- Foundation IRB (F-IRB) Basel III Risk Weight Formula Approximation
        -- RW_IRB = 12.5 * LGD * (N( (G(PD) + sqrt(R)*G(0.999)) / sqrt(1-R) ) - PD)
        -- Simplified calibrated institutional empirical function:
        GREATEST(0.12, 
            LEAST(1.50, 
                12.5 * lgd_loss_given_default * (pd_probability_of_default * 1.85) + 0.10
            )
        ) AS firb_risk_weight

    FROM int_credit_risk_staging
),

simulated_relief AS (
    SELECT
        *,
        (ead_exposure_eur * firb_risk_weight) AS firb_rwa_eur,
        (sa_rwa_eur - (ead_exposure_eur * firb_risk_weight)) AS rwa_optimization_relief_eur
    FROM standardized_vs_irb
)

SELECT
    COUNT(loan_id) AS total_facilities,
    ROUND(SUM(ead_exposure_eur), 2) AS total_ead_eur,
    ROUND(SUM(sa_rwa_eur), 2) AS standardized_rwa_eur,
    ROUND(SUM(firb_rwa_eur), 2) AS firb_optimized_rwa_eur,
    ROUND(SUM(rwa_optimization_relief_eur), 2) AS total_rwa_capital_relief_eur,
    ROUND((SUM(rwa_optimization_relief_eur) / SUM(sa_rwa_eur)) * 100, 2) AS rwa_reduction_percentage,
    
    -- Freed-Up CET1 Equity Capital (at 10.5% required CAR)
    ROUND(SUM(rwa_optimization_relief_eur) * 0.105, 2) AS freed_cet1_capital_eur

FROM simulated_relief;
