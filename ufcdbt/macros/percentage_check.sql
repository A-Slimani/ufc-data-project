{% test percentage_check(model, column_name) %}
    SELECT {{ column_name}}
    FROM {{ model}}
    WHERE {{ column_name }} < 0 OR {{ column_name }} > 100
{% endtest %}