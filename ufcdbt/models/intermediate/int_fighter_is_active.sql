WITH combined_tables AS (
  SELECT
    r_fighter_id AS "id",
    fight_date
  FROM {{ ref('stg_fights') }} f
  UNION
  SELECT
    b_fighter_id AS "id",
    fight_date
  FROM {{ ref('stg_fights') }} 
)
SELECT
  id,
  MAX(fight_date) AS "last_active" 
FROM {{ ref('stg_fights') }}
GROUP BY id 