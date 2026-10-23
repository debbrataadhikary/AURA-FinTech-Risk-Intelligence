-- ==============================================================================
-- SCRIPT 02: Real-Time AML Structuring & Rapid Smurfing Surveillance
-- OBJECTIVE: Detect intentional threshold-evasion transfers (< €10,000 regulatory cap)
-- TECHNIQUES: Rolling Sliding Windows, Lag/Lead Inter-Arrival Delays, Outlier Scoring
-- ==============================================================================

WITH sequence_enrichment AS (
    SELECT
        txn_id,
        customer_id,
        channel,
        amount_eur,
        is_foreign_counterparty,
        is_high_risk_jurisdiction,
        txn_timestamp,
        
        -- Previous transaction timestamp per obligor
        LAG(txn_timestamp, 1) OVER (
            PARTITION BY customer_id 
            ORDER BY txn_timestamp
        ) AS prev_txn_timestamp,

        -- Previous transaction amount
        LAG(amount_eur, 1) OVER (
            PARTITION BY customer_id 
            ORDER BY txn_timestamp
        ) AS prev_amount_eur,

        -- Rolling 48-Hour cumulative flow
        SUM(amount_eur) OVER (
            PARTITION BY customer_id 
            ORDER BY txn_timestamp 
            RANGE BETWEEN INTERVAL 48 HOUR PRECEDING AND CURRENT ROW
        ) AS rolling_48h_volume_eur

    FROM stg_transactions_stream
),

structuring_candidates AS (
    SELECT
        *,
        DATEDIFF('minute', prev_txn_timestamp, txn_timestamp) AS minutes_since_prior_txn,
        CASE
            WHEN amount_eur >= 9000.0 AND amount_eur < 10000.0 
                 AND prev_amount_eur >= 9000.0 AND prev_amount_eur < 10000.0
                 AND DATEDIFF('minute', prev_txn_timestamp, txn_timestamp) <= 180
            THEN 'CONFIRMED_SERIAL_SMURFING'
            WHEN amount_eur >= 9000.0 AND amount_eur < 10000.0
            THEN 'ISOLATED_STRUCTURING_SUSPICION'
            ELSE 'STANDARD_TRANSFER'
        END AS structuring_typology
    FROM sequence_enrichment
)

SELECT
    customer_id,
    COUNT(txn_id) AS total_events,
    COUNT(CASE WHEN structuring_typology = 'CONFIRMED_SERIAL_SMURFING' THEN 1 END) AS smurfing_hit_count,
    ROUND(SUM(amount_eur), 2) AS total_smurfed_flow_eur,
    ROUND(AVG(minutes_since_prior_txn), 1) AS avg_interval_minutes,
    MAX(rolling_48h_volume_eur) AS peak_48h_velocity_eur,
    MAX(is_high_risk_jurisdiction) AS routes_through_fatf_blacklist
FROM structuring_candidates
WHERE structuring_typology IN ('CONFIRMED_SERIAL_SMURFING', 'ISOLATED_STRUCTURING_SUSPICION')
GROUP BY customer_id
HAVING COUNT(txn_id) >= 2
ORDER BY smurfing_hit_count DESC, total_smurfed_flow_eur DESC;
