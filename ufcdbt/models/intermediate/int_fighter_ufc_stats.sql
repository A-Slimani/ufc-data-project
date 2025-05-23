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
  COUNT(CASE WHEN ct.fighter_status = 'Loss' THEN 1 END) AS ufc_losses,
  COUNT(CASE WHEN ct.fighter_status = 'Draw' THEN 1 END) AS ufc_draws,
  COUNT(CASE WHEN ct.fighter_status = 'No Contest' THEN 1 END) AS ufc_no_contests,
  COALESCE(ROUND((COUNT(CASE WHEN ct.fighter_status = 'Win' THEN 1 END)::NUMERIC / NULLIF(COUNT(ct.fighter_status), 0)) * 100, 2), 0.00) AS ufc_win_percentage
FROM combined_tables ct 
JOIN {{ ref('stg_fighters') }} f
ON f.id = ct.fighter_id
GROUP BY ct.fighter_id 