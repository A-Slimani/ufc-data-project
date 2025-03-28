WITH combined_tables AS (
  SELECT 
    f.r_fighter_id AS fighter_id, 
    f.r_fighter_status AS fighter_status
  FROM {{ ref('stg_fights') }} f 
  JOIN {{ ref('stg_events') }} e 
  ON f.event_id = e.id
  UNION ALL 
  SELECT 
    f.b_fighter_id AS fighter_id, 
    f.b_fighter_status AS fighter_status
  FROM {{ ref('stg_fights') }} f 
  JOIN {{ ref('stg_events') }} e 
  ON f.event_id = e.id
) 

SELECT 
  ct.fighter_id, 
  COUNT(ct.fighter_status) AS ufc_fights,
  COUNT(CASE WHEN ct.fighter_status = 'Win' THEN 1 END) AS ufc_wins,
  ROUND((COUNT(CASE WHEN ct.fighter_status = 'Win' THEN 1 END)::NUMERIC / COUNT(*)) * 100, 2) AS ufc_win_percentage
FROM combined_tables ct 
JOIN {{ ref('stg_fighters') }} f
ON f.id = ct.fighter_id
GROUP BY ct.fighter_id 