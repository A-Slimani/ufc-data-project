{% macro time_conversion(col) %}
    (TO_CHAR(MAKE_INTERVAL(secs := {{ col }}), 'HH24:MI:SS'))
{% endmacro %}