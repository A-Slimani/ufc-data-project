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
    f.r_total_control_time_seconds AS "total_control_time_seconds",
    f.r_clinch_control_time_seconds AS "clinch_control_time_seconds",
    f.r_ground_control_time_seconds AS "ground_control_time_seconds"
  FROM
    {{ ref('int_fights_transformations')}} f
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
    f.b_total_control_time_seconds AS "total_control_time_seconds",
    f.b_clinch_control_time_seconds AS "clinch_control_time_seconds",
    f.b_ground_control_time_seconds AS "ground_control_time_seconds"
  FROM
    {{ ref('int_fights_transformations')}} f
  LEFT JOIN
    {{ ref('stg_fighters')}} fs
  ON
    f.b_fighter_id = fs.id
)

SELECT 
  fighter_id,
  SUM(knockdowns::INT) as career_knockdowns,
  SUM(takedowns_attempted::INT) AS career_takedowns_attempted,
  SUM(takedowns_landed::INT) as career_takedowns_landed,
  {{ get_accuracy('takedowns_landed', 'takedowns_attempted') }} AS career_takedown_accuracy,
  SUM(sig_strikes_attempted::INT) AS career_sig_strikes_attempted,
  SUM(sig_strikes_landed::INT) AS career_sig_strikes_landed,
  {{ get_accuracy('total_strikes_landed', 'total_strikes_attempted') }} AS career_total_strike_accuracy,
  SUM(total_strikes_landed::INT) AS career_total_strikes_landed,
  SUM(total_strikes_attempted::INT) AS career_total_strikes_attempted,
  {{ get_accuracy('sig_strikes_landed', 'sig_strikes_attempted') }} AS career_sig_strike_accuracy,
  SUM(submissions_attempted::INT) AS career_submissions_attempted,
  COALESCE(SUM(total_control_time_seconds), 0) AS career_control_time_seconds,
  COALESCE(SUM(clinch_control_time_seconds), 0) AS career_clinch_control_time_seconds,
  COALESCE(SUM(ground_control_time_seconds), 0) AS career_ground_control_time_seconds
FROM combined_ids ci
GROUP BY fighter_id
