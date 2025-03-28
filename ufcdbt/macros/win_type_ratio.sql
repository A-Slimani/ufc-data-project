{% macro win_type_ratio(col) %}
CASE
  WHEN {{ col }} LIKE '%TKO%' THEN 1
  WHEN {{ col }} LIKE 'Dec%' THEN 2 
  WHEN {{ col }} = 'Submission' THEN 3 
  ELSE 0
END
{% endmacro %}