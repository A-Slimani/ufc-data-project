WITH "3_rounders" AS (
  SELECT
    CASE
      WHEN r_fighter_status = 'Win' THEN r_fighter_id 
      WHEN b_fighter_status = 'Win' THEN b_fighter_id
      ELSE NULL
    END AS "fighter_id",
    COUNT(ending_round) AS "3R_finishes",
    COUNT(CASE WHEN ending_round=1 THEN 1 END) AS "3R_1_finishes",
    COUNT(CASE WHEN ending_round=2 THEN 1 END) AS "3R_2_finishes",
    COUNT(CASE WHEN ending_round=3 THEN 1 END) AS "3R_3_finishes"
  FROM {{ ref('stg_fights') }} 
  WHERE bout_rounds=3 AND  method_type IN (1, 2)
  GROUP BY 1
), "5_rounders" AS (
  SELECT
    CASE
      WHEN r_fighter_status = 'Win' THEN r_fighter_id 
      WHEN b_fighter_status = 'Win' THEN b_fighter_id
      ELSE NULL
    END AS "fighter_id",
    COUNT(ending_round) AS "5R_finishes",
    COUNT(CASE WHEN ending_round=1 THEN 1 END) AS "5R_1_finishes",
    COUNT(CASE WHEN ending_round=2 THEN 1 END) AS "5R_2_finishes",
    COUNT(CASE WHEN ending_round=3 THEN 1 END) AS "5R_3_finishes",
    COUNT(CASE WHEN ending_round=4 THEN 1 END) AS "5R_4_finishes",
    COUNT(CASE WHEN ending_round=5 THEN 1 END) AS "5R_5_finishes"
  FROM {{ ref('stg_fights') }} 
  WHERE bout_rounds=5 AND  method_type IN (1, 2)
  GROUP BY 1
)
SELECT
  COALESCE(t.fighter_id, f.fighter_id) AS "fighter_id",
  {{ get_percentage(['"3R_1_finishes"', '"3R_finishes"']) }} AS "3R_1_finish_percentage",
  {{ get_percentage(['"3R_2_finishes"', '"3R_finishes"']) }} AS "3R_2_finish_percentage",
  {{ get_percentage(['"3R_3_finishes"', '"3R_finishes"']) }} AS "3R_3_finish_percentage",
  {{ get_percentage(['"5R_1_finishes"', '"5R_finishes"']) }} AS "5R_1_finish_percentage",
  {{ get_percentage(['"5R_2_finishes"', '"5R_finishes"']) }} AS "5R_2_finish_percentage",
  {{ get_percentage(['"5R_3_finishes"', '"5R_finishes"']) }} AS "5R_3_finish_percentage",
  {{ get_percentage(['"5R_4_finishes"', '"5R_finishes"']) }} AS "5R_4_finish_percentage",
  {{ get_percentage(['"5R_5_finishes"', '"5R_finishes"']) }} AS "5R_5_finish_percentage"
FROM "3_rounders" t
FULL JOIN "5_rounders" f
ON t.fighter_id=f.fighter_id
