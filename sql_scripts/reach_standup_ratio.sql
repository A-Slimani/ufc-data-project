WITH t_values AS (
  SELECT
    r_fighter_id,
    r_fighter_name,
    b_fighter_id,
    b_fighter_name,
    standing_time_seconds AS "standing",
    ground_time_seconds AS "ground",
    clinch_time_seconds AS "clinch"
  FROM dbt_schema.fact_fights f
), ratio_values AS (
  SELECT 
    r_fighter_id,
    r_fighter_name,
    b_fighter_id,
    b_fighter_name,
    standing - clinch AS "striking",
    ground + clinch AS "grappling"
  FROM t_values
), combined_ids AS (
  SELECT
    r_fighter_id, 
    r_fighter_name,
    f.reach AS "r_fighter_reach",
    b_fighter_id,
    b_fighter_name,
    f2.reach AS "b_fighter_reach",
    striking,
    grappling,
    ROUND(striking::NUMERIC / (striking + grappling), 2) AS "ratio"
  FROM ratio_values r 
  LEFT JOIN dbt_schema.dim_fighters f ON r.r_fighter_id = f.fighter_id
  LEFT JOIN dbt_schema.dim_fighters f2 ON r.b_fighter_id = f2.fighter_id
)
SELECT COUNT(*) FROM combined_ids
-- SELECT 
--   r_fighter_id,
--   striking,
--   grappling,
--   ROUND(striking::NUMERIC / (striking + grappling), 2) AS "ratio"
-- FROM ratio_values

-- SELECT
--   ROUND(striking::NUMERIC / (striking + grappling), 2) * 100 AS "ratio",
--   COUNT(ROUND(striking::NUMERIC / (striking + grappling), 2)) 
-- FROM ratio_values
-- GROUP BY ratio
-- ORDER BY ratio


