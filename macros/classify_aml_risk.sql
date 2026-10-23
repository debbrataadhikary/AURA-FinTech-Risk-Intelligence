{% macro classify_aml_risk(velocity_count, amount, is_foreign, is_high_risk, structuring_flag) %}
    CASE 
        WHEN {{ structuring_flag }} = 1 THEN 'CRITICAL_STRUCTURING'
        WHEN {{ is_high_risk }} = 1 AND {{ amount }} > 15000 THEN 'HIGH_RISK_JURISDICTION_LARGE'
        WHEN {{ velocity_count }} >= 6 AND {{ amount }} > 5000 THEN 'HIGH_VELOCITY_BURST'
        WHEN {{ is_foreign }} = 1 AND {{ amount }} > 25000 THEN 'MEDIUM_CROSS_BORDER'
        ELSE 'LOW_MONITORED'
    END
{% endmacro %}
