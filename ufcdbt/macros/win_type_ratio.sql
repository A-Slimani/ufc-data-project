{% macro fight_result_type(col) %}
CASE
  WHEN {{ col }} LIKE '%TKO%' THEN 1
  WHEN {{ col }} = 'Submission' THEN 2 
  WHEN {{ col }} LIKE 'Dec%' THEN 3 
  ELSE 0
END
{% endmacro %}