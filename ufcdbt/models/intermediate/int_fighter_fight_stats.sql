WITH combined_ids AS (
  SELECT
    f.id AS "fight_id",
    f.r_fighter_id AS "fighter_id",
    f.r_knockdowns AS "knockdowns",
    f.r_takedowns_landed AS "takedowns_landed",
    f.r_takedowns_attempted AS "takedowns_attempted",
    f.r_sig_strikes_landed AS "sig_strikes_landed",
    f.r_sig_strikes_attempted AS "sig_strikes_attempted",
    f.r_sig_strikes_accuracy AS "sig_strikes_accuracy",
    f.r_total_strikes_landed AS "total_strikes_landed",
    f.r_total_strikes_attempted AS "total_strikes_attempted",
    f.r_submissions_attempted AS "submissions_attempted",
    f.r_control_time AS "control_time",
    f.r_clinch_control_time AS "clinch_control_time",
    f.r_ground_control_time AS "ground_control_time"
  FROM
    {{ ref('stg_fights')}} f
  LEFT JOIN
    {{ ref('stg_fighters')}} fs
  ON
    f.r_fighter_id = fs.id
  UNION ALL
  SELECT
    f.id AS "fight_id",
    f.b_fighter_id AS "fighter_id",
    f.b_knockdowns AS "knockdowns",
    f.b_takedowns_landed AS "takedowns_landed",
    f.b_takedowns_attempted AS "takedowns_attempted",
    f.b_sig_strikes_landed AS "sig_strikes_landed",
    f.b_sig_strikes_attempted AS "sig_strikes_attempted",
    f.b_sig_strikes_accuracy AS "sig_strikes_accuracy",
    f.b_total_strikes_landed AS "total_strikes_landed",
    f.b_total_strikes_attempted AS "total_strikes_attempted",
    f.b_submissions_attempted AS "submissions_attempted",
    f.b_control_time AS "control_time",
    f.b_clinch_control_time AS "clinch_control_time",
    f.b_ground_control_time AS "ground_control_time"
  FROM
    {{ ref('stg_fights')}} f
  LEFT JOIN
    {{ ref('stg_fighters')}} fs
  ON
    f.b_fighter_id = fs.id
)

SELECT 
  fighter_id,
  SUM(knockdowns::NUMERIC) as career_knockdowns,
  SUM(takedowns_landed::NUMERIC) as career_takedowns_landed,
  SUM(takedowns_attempted::NUMERIC) AS career_takedowns_attempted,
  ROUND(SUM(takedowns_landed::NUMERIC) / NULLIF(SUM(takedowns_attempted::NUMERIC), 0) * 100, 2) AS career_takedown_accuracy,
  SUM(sig_strikes_landed::NUMERIC) AS career_sig_strikes_landed,
  SUM(sig_strikes_attempted::NUMERIC) AS career_sig_strikes_attempted,
  ROUND(SUM(sig_strikes_landed::NUMERIC) / NULLIF(SUM(sig_strikes_attempted::NUMERIC), 0) * 100, 2) AS career_sig_strike_accuracy,
  SUM(total_strikes_landed::NUMERIC) AS career_total_strikes_landed,
  SUM(total_strikes_attempted::NUMERIC) AS career_total_strikes_attempted,
  ROUND(SUM(total_strikes_landed::NUMERIC) / NULLIF(SUM(total_strikes_attempted::NUMERIC), 0) * 100, 2) AS career_total_strike_accuracy,
  SUM(submissions_attempted::NUMERIC) AS career_submissions_attempted,
  SUM(EXTRACT(EPOCH FROM control_time::INTERVAL)::NUMERIC) AS career_control_time_seconds,
  SUM(EXTRACT(EPOCH FROM clinch_control_time::INTERVAL)::NUMERIC) AS career_clinch_control_time_seconds,
  SUM(EXTRACT(EPOCH FROM ground_control_time::INTERVAL)::NUMERIC) AS career_ground_control_time_seconds
FROM combined_ids ci
GROUP BY fighter_id
