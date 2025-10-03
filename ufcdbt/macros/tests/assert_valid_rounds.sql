{% test assert_two_rounds_limit(model, column_name)%}
SELECT * FROM {{ model }}
WHERE
  fight_date > '2002-01-01'
  AND
  {{ column_name }} = 2
{% endtest %}
