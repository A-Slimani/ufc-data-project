-- count the fights with designated rounds
SELECT 
  bout_rounds,
  CASE 
    WHEN method_type=1 THEN 'KO/TKO'
    ELSE 'SUBMISSION' 
  END,
  COUNT(bout_rounds)
FROM dbt_schema.fact_fights
WHERE 
  (bout_rounds=5 OR bout_rounds=3)
  AND
  (method_type=1 OR method_type=2)
GROUP BY bout_rounds, method_type

-- ratio of finishes 
WITH fight_counts AS (
  SELECT
    bout_rounds,
    COUNT(CASE WHEN method_type=1 THEN 1 END) AS "ko_tko_count",
    COUNT(CASE WHEN method_type=2 THEN 1 END) AS "sub_count",
    COUNT(bout_rounds) AS "overall"
  FROM dbt_schema.fact_fights
  WHERE bout_rounds=5 OR bout_rounds=3
  GROUP BY bout_rounds
)
SELECT
  bout_rounds,
  ROUND(ko_tko_count::NUMERIC / overall, 2) AS "ko_tko_percentage",
  ROUND(sub_count::NUMERIC / overall, 2) AS "sub_percentage",
  ROUND((sub_count + ko_tko_count)::NUMERIC / overall, 2) AS "overall_finish_percentage"
FROM fight_counts


-- finishes over different rounds
WITH finish_count AS (
  SELECT
    bout_rounds,
    ending_round,
    COUNT(CASE WHEN method_type=1 THEN 1 END) AS "ko_tko_count",
    COUNT(CASE WHEN method_type=2 THEN 1 END) AS "sub_count"
  FROM dbt_schema.fact_fights
  WHERE bout_rounds IN (3, 5)
  GROUP BY bout_rounds, ending_round 
),
total AS (
  SELECT
    bout_rounds,
    COUNT(bout_rounds) AS total_fights
  FROM dbt_schema.fact_fights
  WHERE bout_rounds IN (3, 5)
  GROUP BY bout_rounds
)
SELECT
  c.bout_rounds,
  ending_round,
  ko_tko_count,
  sub_count,
  total_fights,
  ROUND(ko_tko_count * 100.0 / total_fights, 2) AS "ko_tko_percentage",
  ROUND(sub_count * 100.0 / total_fights, 2) AS "sub_percentage",
  ROUND((ko_tko_count + sub_count) * 100.0 / total_fights, 2) AS "total_percentage"
FROM finish_count c
LEFT JOIN total t 
ON c.bout_rounds = t.bout_rounds
ORDER BY bout_rounds, ending_round

-- finishes over different weight classes
WITH finish_count AS (
  SELECT
    bout_weight_id,
    bout_weight,
    bout_rounds,
    ending_round,
    COUNT(CASE WHEN method_type=1 THEN 1 END) AS "ko_tko_count",
    COUNT(CASE WHEN method_type=2 THEN 1 END) AS "sub_count"
  FROM dbt_schema.fact_fights
  WHERE bout_rounds IN (3, 5)
  GROUP BY bout_weight_id, bout_weight, bout_rounds, ending_round
),
total AS (
  SELECT
    bout_weight,
    bout_rounds,
    COUNT(*) AS total_fights
  FROM dbt_schema.fact_fights
  WHERE bout_rounds IN (3, 5) 
  GROUP BY bout_weight, bout_rounds
)
SELECT
  c.bout_weight_id,
  c.bout_weight,
  c.bout_rounds,
  c.ending_round,
  ROUND(ko_tko_count::NUMERIC / total_fights, 2) AS "ko_tko_percentage",
  ROUND(sub_count::NUMERIC / total_fights, 2) AS "sub_percenatge",
  ROUND((ko_tko_count + sub_count)::NUMERIC / total_fights, 2) AS "total_percentage"
FROM finish_count c
LEFT JOIN total t 
ON 
  c.bout_weight = t.bout_weight 
  AND 
  c.bout_rounds = t.bout_rounds
WHERE c.bout_weight_id < 100 AND total_fights >= 10
ORDER BY c.bout_weight_id, c.bout_rounds, c.ending_round
