{% macro generate_wins_by_type(method) %}
    COUNT(CASE WHEN {{ method }} IN ('U-DEC', 'S-DEC') THEN 1 END) as total_wins_by_dec,
    COUNT(CASE WHEN {{ method }} = 'U-DEC' THEN 1 END) as total_wins_by_unanimous_dec,
    COUNT(CASE WHEN {{ method }} = 'S-DEC' THEN 1 END) as total_wins_by_split_dec,
    COUNT(CASE WHEN {{ method }} = 'KO/TKO' THEN 1 END) as total_wins_by_ko_tko,
    COUNT(CASE WHEN {{ method }} = 'SUB' THEN 1 END) as total_wins_by_sub
{% endmacro %}