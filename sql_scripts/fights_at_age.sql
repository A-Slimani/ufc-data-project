SELECT 
  a.fight_date,
  (EXTRACT(YEAR FROM CURRENT_DATE) - EXTRACT(YEAR FROM a.fight_date)) AS "difference_from_today",
  b.full_name AS "r_fighter_name",
  b.age AS "r_current_age",
  b.age - (EXTRACT(YEAR FROM CURRENT_DATE) - EXTRACT(YEAR FROM a.fight_date)) AS "r_age_at_time",
  c.full_name AS "b_fighter_name", 
  c.age AS "b_current_age"
  c.age - (EXTRACT(YEAR FROM CURRENT_DATE) - EXTRACT(YEAR FROM a.fight_date)) AS "b_age_at_time",
FROM dbt_schema.stg_fights a
lEFT JOIN dbt_schema.stg_fighters b
ON a.r_fighter_id = b.id
LEFT JOIN dbt_schema.stg_fighters c
ON a.b_fighter_id = c.id