with combined AS (
  SELECT
    r_fighter_id AS "fighter_id",
    ending_round,
    bout_rounds,
    r_fighter_status,
    b_fighter_status
  FROM dbt_schema.fact_fights
  UNION ALL
  SELECT
    b_fighter_id AS "fighter_id",
    ending_round,
    bout_rounds,
    r_fighter_status,
    b_fighter_status
  FROM dbt_schema.fact_fights
)
SELECT
  f.fighter_id,
  f.full_name,
  ending_round,
  r_fighter_status,
  b_fighter_status,
  COUNT(ending_round)
FROM combined c
JOIN dbt_schema.dim_fighters f
ON f.fighter_id = c.fighter_id
WHERE bout_rounds=3
GROUP BY f.fighter_id, f.full_name, ending_round 
ORDER BY f.fighter_id, ending_round

-- with fight status included
WITH combined_3 AS (
  SELECT
    r_fighter_name AS fighter_name,
    ending_round,
    r_fighter_status AS status
  FROM dbt_schema.fact_fights
  WHERE bout_rounds = 3
  UNION ALL
  SELECT
    b_fighter_name AS fighter_name,
    ending_round,
    b_fighter_status AS status
  FROM dbt_schema.fact_fights
  WHERE bout_rounds = 3
),
count_table AS (
  SELECT
    fighter_name,
    ending_round,
    COUNT(*) AS fight_count,
    COUNT(CASE WHEN status = 'Win' THEN 1 END) AS win_count,
    COUNT(CASE WHEN status = 'Loss' THEN 1 END) AS loss_count,
    COUNT(CASE WHEN status = 'Draw' THEN 1 END) AS draw_count,
    COUNT(CASE WHEN status = 'No Contest' THEN 1 END) AS no_contest_count
  FROM combined_3
  GROUP BY fighter_name, ending_round
  ORDER BY fighter_name, ending_round
),
sum_table AS (
  SELECT
    fighter_name,
    SUM(fight_count) AS "total_sum",
    SUM(win_count) AS "win_sum",
    SUM(loss_count) AS "loss_sum"
  FROM count_table
  GROUP BY fighter_name 
  ORDER BY fighter_name
)
SELECT
  c.fighter_name,
  c.ending_round,
  COALESCE(ROUND(c.fight_count::NUMERIC / NULLIF(s.total_sum, 0), 2), 0) AS "round_percentage",
  COALESCE(ROUND(c.win_count::NUMERIC / NULLIF(s.win_sum, 0), 2), 0) AS "win_percentage"
  COALESCE(ROUND(c.loss_count::NUMERIC / NULLIF(s.loss_sum, 0), 2), 0) AS "win_percentage"
FROM count_table c
JOIN sum_table s
ON c.fighter_name = s.fighter_name
