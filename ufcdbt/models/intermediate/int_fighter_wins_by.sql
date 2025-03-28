WITH winning_fighter AS (
  SELECT
    method_type,
    CASE
      WHEN r_fighter_status = 'Win' THEN r_fighter_id 
      WHEN b_fighter_status = 'Win' THEN b_fighter_id
      ElSE NULL 
    END AS "fighter_id"
  FROM {{ ref('stg_fights')}}
)
SELECT 
  a.fighter_id,
  COUNT(method_type) AS "wins",
  COUNT(CASE WHEN a.method_type=1 THEN 1 END) AS ko_tko, 
  COUNT(CASE WHEN a.method_type=2 THEN 1 END) AS dec, 
  COUNT(CASE WHEN a.method_type=3 THEN 1 END) AS sub 
FROM winning_fighter a
LEFT JOIN {{ ref('stg_fighters') }} b
ON a.fighter_id = b.id
WHERE a.method_type IS NOT NULL
GROUP BY a.fighter_id