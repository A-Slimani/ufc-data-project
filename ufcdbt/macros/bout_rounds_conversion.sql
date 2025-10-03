{% macro bout_rounds_conversion(column) %}
  CASE
    WHEN {{ column }} = 4 THEN 3
    ELSE {{ column }}
  END
{% endmacro %}
