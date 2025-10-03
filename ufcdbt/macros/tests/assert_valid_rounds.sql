{% test assert_valid_rounds(model, column_name)%}
SELECT * FROM {{ model }}
WHERE
  fight_date > '2002-01-01'
  AND
  {{ column_name }} NOT IN (3, 5)
{% endtest %}
