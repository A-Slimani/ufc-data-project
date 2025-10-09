WITH seconds_table AS (
  SELECT
    ending_round,
    EXTRACT(MINUTE FROM ('00:' || time)::INTERVAL) AS "fight_minutes",
    EXTRACT(SECOND FROM ('00:' || time)::INTERVAL) AS "fight_seconds",
    time,
    method,
    ground_time_seconds AS "g",
    standing_time_seconds AS "s",
    clinch_time_seconds AS "c"
  FROM 
    dbt_schema.fact_fights
), calculated_seconds AS (
  SELECT
    ((ending_round - 1) * 5 * 60) + (fight_minutes * 60) + (fight_seconds) AS "total_seconds",
    g + s AS "total_seconds_by_combined"
  FROM seconds_table 
), diff_table AS (
  SELECT
    total_seconds,
    total_seconds_by_combined,
    ABS(total_seconds - total_seconds_by_combined) AS "difference"
  FROM calculated_seconds
)
SELECT
  AVG(difference) AS "mean",
  STDDEV(difference) AS "standard_deviation",
  MAX(difference) AS "max_difference"
FROM diff_table

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
SELECT
  
FROM seconds_table
