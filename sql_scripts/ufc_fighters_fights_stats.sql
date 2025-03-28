WITH merged_table AS (
  SELECT 
  	f.r_fighter_id AS "fighter_id", 
  	f.r_fighter_status AS "fighter_status"
  FROM fights f 
  JOIN dbt_schema.ufc_events e 
  ON f.event_id = e.id
  UNION ALL 
  SELECT 
  	f.b_fighter_id AS "fighter_id", 
  	f.b_fighter_status AS "fighter_status"
  FROM fights f 
  JOIN dbt_schema.ufc_events e 
  ON f.event_id = e.id
)
SELECT 
  f.id,
  COUNT(m.fighter_status) AS "ufc_fights",
  COUNT(CASE WHEN m.fighter_status = 'Win' THEN 1 END) AS "ufc_wins",
  ROUND((COUNT(CASE WHEN m.fighter_status THEN 1 END)::NUMERIC / COUNT(*)) * 100, 2) AS "ufc_win_percentage"
FROM merged_table m
LEFT JOIN fighters f
ON f.id = m.fighter_id
GROUP BY f.id