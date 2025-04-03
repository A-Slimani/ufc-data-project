{% macro country_fix(col_name) %}
  CASE 
    WHEN LOWER({{ col_name }}) = 'usa' THEN 'United States' 
    ELSE {{ col_name }} 
  END AS {{ col_name }} 
{% endmacro %}
-- redundant now I just get the data from the 
-- new tricode columns