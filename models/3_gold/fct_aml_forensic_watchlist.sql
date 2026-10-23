{{ config(materialized='table') }}

WITH silver_aml AS (
    SELECT * FROM {{ ref('int_aml_behavioral_metrics') }}
)

SELECT
    customer_id,
    COUNT(txn_id) AS total_monitored_txns,
    ROUND(SUM(amount_eur), 2) AS total_volume_flow_eur,
    ROUND(AVG(amount_eur), 2) AS avg_txn_flow_eur,
    MAX(hourly_velocity_count) AS peak_hourly_velocity,
    SUM(is_foreign_counterparty) AS total_cross_border_txns,
    SUM(is_high_risk_jurisdiction) AS total_high_risk_geo_txns,
    SUM(is_structuring_threshold_evasion) AS structuring_evasion_hits,
    MAX(composite_aml_risk_score) AS max_composite_risk_score,

    -- Forensic Audit Priority
    CASE
        WHEN MAX(composite_aml_risk_score) >= 75 OR SUM(is_structuring_threshold_evasion) >= 2 
            THEN 'TIER_1_IMMEDIATE_SAR_FILING'
        WHEN MAX(composite_aml_risk_score) >= 50 OR SUM(is_high_risk_jurisdiction) >= 1 
            THEN 'TIER_2_ENHANCED_DUE_DILIGENCE'
        ELSE 'TIER_3_ROUTINE_MONITORING'
    END AS forensic_investigation_priority

FROM silver_aml
GROUP BY customer_id
HAVING MAX(composite_aml_risk_score) >= 40.0
ORDER BY max_composite_risk_score DESC, total_volume_flow_eur DESC
