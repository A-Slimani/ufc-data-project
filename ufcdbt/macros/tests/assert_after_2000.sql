{% test assert_after_2000(model, column_name) %}
SELECT * FROM {{ model }}
WHERE {{ column_name }} < '2000-01-01'
{% endtest %}
