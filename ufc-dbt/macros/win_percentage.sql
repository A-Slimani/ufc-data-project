{% macro generate_win_percentage(wins, losses, draws) %}
    CASE 
        WHEN ({{ wins }} + {{ losses }} + {{ draws }}) = 0 THEN 0
        ELSE ROUND({{ wins }}::NUMERIC / ({{ wins }} + {{ losses }} + {{ draws }}) * 100, 2)
    END 
{% endmacro %}