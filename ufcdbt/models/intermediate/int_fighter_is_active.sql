WITH combined_tables AS (
  SELECT
    r_fighter_id AS "id",
    r_fighter_name AS "full_name",
    fight_date
  FROM {{ ref('stg_fights') }} f
  UNION
  SELECT
    b_fighter_id AS "id",
    b_fighter_name AS "full_name",
    fight_date
  FROM {{ ref('stg_fights') }} 
)
SELECT
  id,
  full_name,
  MAX(fight_date) AS "last_active" 
FROM {{ ref('stg_fights') }}
GROUP BY id, full_name