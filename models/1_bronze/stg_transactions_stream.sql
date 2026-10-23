{{ config(materialized='view') }}

WITH raw_transactions AS (
    SELECT * FROM {{ source('aura_raw', 'fact_transactions_stream') }}
)

SELECT
    CAST(transaction_id AS VARCHAR) AS txn_id,
    CAST(customer_id AS VARCHAR) AS customer_id,
    UPPER(TRIM(CAST(channel AS VARCHAR))) AS channel,
    CAST(amount_eur AS DOUBLE) AS amount_eur,
    CAST(is_foreign_counterparty AS INTEGER) AS is_foreign_counterparty,
    CAST(is_high_risk_jurisdiction AS INTEGER) AS is_high_risk_jurisdiction,
    CAST(hourly_velocity_count AS INTEGER) AS hourly_velocity_count,
    CAST(aml_suspicious_flag AS INTEGER) AS aml_suspicious_flag,
    CAST(timestamp AS TIMESTAMP) AS txn_timestamp
FROM raw_transactions
WHERE transaction_id IS NOT NULL
