{% macro get_accuracy(landed, attempted) %}
    COALESCE(ROUND(SUM({{ landed }})::NUMERIC / NULLIF(SUM({{ attempted }}), 0) * 100, 2), 0) 
{% endmacro %}