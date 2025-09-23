SELECT
  f.r_fighter_id,
  f.r_fighter_name,
  f.b_fighter_id,
  f.b_fighter_name
FROM dbt_schema.fact_fights f
