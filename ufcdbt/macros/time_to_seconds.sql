{% macro time_to_seconds(col) %}
    (
        split_part({{ col }}, ':', 1)::NUMERIC * 60 
        + 
        split_part({{ col }}, ':', 2)::NUMERIC
    )   
{% endmacro %}