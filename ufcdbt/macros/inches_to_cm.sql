{% macro inches_to_cm(col) %}
  CASE 
    WHEN {{ col }} IS NOT NULL THEN ROUND({{ col }} * 2.54)
    ELSE NULL
  END AS {{ col }}
{% endmacro %}
