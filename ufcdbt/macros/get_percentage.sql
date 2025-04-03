{% macro get_percentage(columns) %}
  CASE
    WHEN ({{ columns | join(' + ')}}) = 0 THEN 0
    ELSE ROUND({{columns[0]}}::NUMERIC / ({{ columns | join(' + ')}}) * 100, 2)
  END 
{% endmacro %}
 