{% macro generate_weight_class_id(description) %}
  CASE 
    WHEN {{ description }} = 'Heavyweight' THEN 1 
    WHEN {{ description }} = 'Light Heavyweight' THEN 2 
    WHEN {{ description }} = 'Middleweight' THEN 3 
    WHEN {{ description }} = 'Welterweight' THEN 4 
    WHEN {{ description }} = 'Lightweight' THEN 5 
    WHEN {{ description }} = 'Featherweight' THEN 6 
    WHEN {{ description }} = 'Bantamweight' THEN 7 
    WHEN {{ description }} = 'Flyweight' THEN 8 
    WHEN {{ description }} = 'Women''s Featherweight' THEN 9 
    WHEN {{ description }} = 'Women''s Bantamweight' THEN 10 
    WHEN {{ description }} = 'Women''s Flyweight' THEN 11 
    WHEN {{ description }} = 'Women''s Strawweight' THEN 12 
    ELSE 100
  END 
{% endmacro %}
