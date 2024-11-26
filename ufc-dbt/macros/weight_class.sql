{% macro generate_weight_classes(weight) %}
    CASE
        WHEN  substring({{ weight }}, 1, 3)::NUMERIC  <= 115 THEN 'Strawweight'
        WHEN  substring({{ weight }}, 1, 3)::NUMERIC  <= 125 THEN 'Flyweight'
        WHEN  substring({{ weight }}, 1, 3)::NUMERIC  <= 135 THEN 'Bantamweight'
        WHEN  substring({{ weight }}, 1, 3)::NUMERIC  <= 145 THEN 'Featherweight'
        WHEN  substring({{ weight }}, 1, 3)::NUMERIC  <= 155 THEN 'Lightweight'
        WHEN  substring({{ weight }}, 1, 3)::NUMERIC  <= 170 THEN 'Welterweight'
        WHEN  substring({{ weight }}, 1, 3)::NUMERIC  <= 185 THEN 'Middleweight'
        WHEN  substring({{ weight }}, 1, 3)::NUMERIC  <= 205 THEN 'Light Heavyweight'
        ELSE 'Heavyweight'
    END
{% endmacro %}