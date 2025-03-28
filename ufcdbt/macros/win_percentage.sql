{% macro win_percentage(c1, c2, c3) %}
  CASE
    WHEN ({{c1}} + {{c2}} + {{c3}}) = 0 THEN 0
    ELSE ROUND({{c1}}::NUMERIC / ({{c1}} + {{c2}} + {{c3}}) * 100, 2)
  END AS "win_percentage"
{% endmacro %}
 