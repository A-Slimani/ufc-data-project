
WITH seconds_table AS (
  SELECT
    id,
    r_fighter_name,
    b_fighter_name,
    event_id,
    ending_round,
    EXTRACT(EPOCH FROM ('00: ' || time)::INTERVAL)::INT,
    method,
    ground_time_seconds AS "g",
    standing_time_seconds AS "s",
    clinch_time_seconds AS "c"
  FROM 
    dbt_schema.fact_fights
)

-- clinch included in standing
SELECT 
  g + s AS "total",
  r_fighter_name,
  b_fighter_name,
  event_id,
  ending_round,
  time,
  method
FROM seconds_table
ORDER BY total

-- clinch separate
SELECT g + s + c AS "total" FROM seconds_table
WHERE g + s + c > 900

-- seconds difference

