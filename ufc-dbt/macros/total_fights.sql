{% macro generate_total_fights(wins, losses, draws) %}
    {{ wins }} + {{ losses }} + {{ draws }} 
{% endmacro %}