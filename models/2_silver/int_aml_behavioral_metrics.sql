{{ config(materialized='table') }}

WITH staged_txns AS (
    SELECT * FROM {{ ref('stg_transactions_stream') }}
),

windowed_metrics AS (
    SELECT
        txn_id,
        customer_id,
        channel,
        amount_eur,
        is_foreign_counterparty,
        is_high_risk_jurisdiction,
        hourly_velocity_count,
        aml_suspicious_flag,
        txn_timestamp,

        -- Customer Lifetime and Benchmark Window Stats
        AVG(amount_eur) OVER (
            PARTITION BY customer_id
        ) AS avg_customer_txn_amount,

        STDDEV(amount_eur) OVER (
            PARTITION BY customer_id
        ) AS stddev_customer_txn_amount,

        -- Dense Rank of Transaction Sizes per Customer
        DENSE_RANK() OVER (
            PARTITION BY customer_id 
            ORDER BY amount_eur DESC
        ) AS txn_size_rank,

        -- Detect Structuring (Smurfing immediately beneath €10,000 reporting threshold)
        CASE 
            WHEN amount_eur >= 9000.0 AND amount_eur < 10000.0 THEN 1 
            ELSE 0 
        END AS is_structuring_threshold_evasion

    FROM staged_txns
),

scored_metrics AS (
    SELECT
        *,
        -- Normalized Amount Deviation (Z-Score)
        CASE 
            WHEN stddev_customer_txn_amount IS NOT NULL AND stddev_customer_txn_amount > 0 
            THEN (amount_eur - avg_customer_txn_amount) / stddev_customer_txn_amount
            ELSE 0.0
        END AS amount_z_score,

        -- AML Regulatory Classification via Macro
        {{ classify_aml_risk('hourly_velocity_count', 'amount_eur', 'is_foreign_counterparty', 'is_high_risk_jurisdiction', 'is_structuring_threshold_evasion') }} AS aml_risk_classification,

        -- Composite AML Risk Index (0 - 100)
        ROUND(
            LEAST(100.0, 
                (hourly_velocity_count * 8.5) + 
                (is_high_risk_jurisdiction * 35.0) + 
                (is_foreign_counterparty * 15.0) + 
                (is_structuring_threshold_evasion * 40.0) +
                (CASE WHEN amount_eur > 20000 THEN 20.0 ELSE 0.0 END)
            ), 2
        ) AS composite_aml_risk_score

    FROM windowed_metrics
)

SELECT * FROM scored_metrics
