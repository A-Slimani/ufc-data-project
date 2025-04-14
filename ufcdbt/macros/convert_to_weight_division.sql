{% macro convert_to_weight_division(weight_col) %}
    CASE
        WHEN {{ weight_col }} = 0 THEN NULL
        WHEN {{ weight_col }} <= 115 THEN 'Strawweight'
        WHEN {{ weight_col }} <= 125 THEN 'Flyweight'
        WHEN {{ weight_col }} <= 135 THEN 'Bantamweight'
        WHEN {{ weight_col }} <= 145 THEN 'Featherweight'
        WHEN {{ weight_col }} <= 155 THEN 'Lightweight'
        WHEN {{ weight_col }} <= 170 THEN 'Welterweight'
        WHEN {{ weight_col }} <= 185 THEN 'Middleweight'
        WHEN {{ weight_col }} <= 205 THEN 'Light Heavyweight'
        ELSE 'Heavyweight'
    END 
{% endmacro %}
-- not using currently