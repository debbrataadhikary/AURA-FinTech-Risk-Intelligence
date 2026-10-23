{{ config(materialized='view') }}

WITH raw_macro AS (
    SELECT * FROM {{ source('aura_raw', 'dim_macro_stress_scenarios') }}
)

SELECT
    UPPER(TRIM(CAST(scenario AS VARCHAR))) AS scenario_name,
    CAST(gdp_growth_pct AS DOUBLE) AS gdp_growth_pct,
    CAST(inflation_hicp_pct AS DOUBLE) AS inflation_hicp_pct,
    CAST(central_bank_rate_pct AS DOUBLE) AS central_bank_rate_pct,
    CAST(unemployment_pct AS DOUBLE) AS unemployment_pct,
    CAST(ecl_stress_multiplier AS DOUBLE) AS ecl_stress_multiplier
FROM raw_macro
