WITH t_values AS (
  SELECT
    r_fighter_id,
    b_fighter_id,
    standing_time_seconds AS "standing",
    ground_time_seconds AS "ground",
    clinch_time_seconds AS "clinch"
  FROM dbt_schema.fact_fights f
  LEFT JOIN dbt_schema.dim_fighters d
), ratio_values AS (
  SELECT 
    r_fighter_name,
    b_fighter_name,
    standing - clinch AS "striking",
    ground + clinch AS "grappling"
  FROM t_values
)
-- SELECT 
--   r_fighter_name,
--   b_fighter_name,
--   striking,
--   grappling,
--   ROUND(striking::NUMERIC / (striking + grappling), 2) AS "ratio"
-- FROM ratio_values
-- ORDER BY ratio
SELECT
  ROUND(striking::NUMERIC / (striking + grappling), 2) * 100 AS "ratio",
  COUNT(ROUND(striking::NUMERIC / (striking + grappling), 2)) 
FROM ratio_values
GROUP BY ratio
ORDER BY ratio

-- GET REACH

