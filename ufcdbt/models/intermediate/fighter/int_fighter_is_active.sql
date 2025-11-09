WITH combined_tables AS (
  SELECT
    r_fighter_id AS "fighter_id",
    fight_date
  FROM {{ ref('int_fights_transformations') }} f
  UNION ALL
  SELECT
    b_fighter_id AS "fighter_id",
    fight_date
  FROM {{ ref('int_fights_transformations') }} 
)
SELECT
  fighter_id,
  MAX(fight_date) AS "last_active" 
FROM combined_tables
GROUP BY fighter_id 