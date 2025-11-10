-- calculating what round a fighter wins / loses
-- This is only for 3 round fights
WITH counts AS (
  SELECT
    r_fighter_id AS "fighter_id",
    COUNT(CASE WHEN ending_round=1 THEN 1 END) AS "r1_finish",
    COUNT(CASE WHEN ending_round=2 THEN 1 END) AS "r2_finish",
    COUNT(CASE WHEN ending_round=3 THEN 1 END) AS "r3_finish"
  FROM dbt_schema.fact_fights
  WHERE 
    bout_rounds=3 AND 
    r_fighter_status='Win' AND 
    method_type IN (1, 2)
  GROUP BY fighter_id
  UNION ALL
  SELECT
    b_fighter_id AS "fighter_id",
    COUNT(CASE WHEN ending_round=1 THEN 1 END) AS "r1_finish",
    COUNT(CASE WHEN ending_round=2 THEN 1 END) AS "r2_finish",
    COUNT(CASE WHEN ending_round=3 THEN 1 END) AS "r3_finish"
  FROM dbt_schema.fact_fights
  WHERE 
    bout_rounds=3 AND 
    b_fighter_status='Win' AND
    method_type IN (1, 2)
  GROUP BY fighter_id
)
SELECT
  fighter_id,
  SUM(r1_finish) AS "r1_finish",
  SUM(r2_finish) AS "r2_finish",
  SUM(r3_finish) AS "r3_finish"
FROM counts 
GROUP BY fighter_id

-- improved version of the script above
-- since I am only using the winning fighter_id I dont need to use UNION
SELECT
  CASE
    WHEN r_fighter_status = 'Win' THEN r_fighter_id 
    WHEN b_fighter_status = 'Win' THEN b_fighter_id
    ELSE NULL
  END AS "fighter_id",
  COUNT(CASE WHEN ending_round=1 THEN 1 END) AS "3R_1_finishes",
  COUNT(CASE WHEN ending_round=2 THEN 1 END) AS "3R_2_finishes",
  COUNT(CASE WHEN ending_round=3 THEN 1 END) AS "3R_3_finishes"
FROM dbt_schema.fact_fights
WHERE bout_rounds=3 AND  method_type IN (1, 2)
GROUP BY 1

-- for 5 rounders
SELECT
  CASE
    WHEN r_fighter_status = 'Win' THEN r_fighter_id 
    WHEN b_fighter_status = 'Win' THEN b_fighter_id
    ELSE NULL
  END AS "fighter_id",
  COUNT(CASE WHEN ending_round=1 THEN 1 END) AS "5R_1_finishes",
  COUNT(CASE WHEN ending_round=2 THEN 1 END) AS "5R_2_finishes",
  COUNT(CASE WHEN ending_round=3 THEN 1 END) AS "5R_3_finishes",
  COUNT(CASE WHEN ending_round=4 THEN 1 END) AS "5R_4_finishes",
  COUNT(CASE WHEN ending_round=5 THEN 1 END) AS "5R_5_finishes"
FROM dbt_schema.fact_fights
WHERE bout_rounds=5 AND  method_type IN (1, 2)
GROUP BY 1
