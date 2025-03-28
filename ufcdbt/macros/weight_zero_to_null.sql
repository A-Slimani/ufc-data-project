{% macro weight_zero_to_null(weight_val) %}
CASE
  WHEN {{ weight_val }} = 0 THEN NULL 
  ELSE {{ weight_val }}
END AS "weight"
{% endmacro %}