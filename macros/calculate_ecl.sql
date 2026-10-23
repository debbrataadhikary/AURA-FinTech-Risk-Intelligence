{% macro calculate_ecl(ead, pd, lgd, discount_rate=0.035, tenor_years=1.0) %}
    ({{ ead }} * {{ pd }} * {{ lgd }} / POWER(1 + {{ discount_rate }}, {{ tenor_years }}))
{% endmacro %}
