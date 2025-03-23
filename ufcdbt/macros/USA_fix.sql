{% macro update_country_name_usa(col_name)%}
  CASE WHEN LOWER(col_name) = 'usa' THEN 'United States'
{% endmacro %}