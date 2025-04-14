SELECT
  id,
  event_id,
  r_fighter_id,
  r_fighter_status,
  b_fighter_id,
  b_fighter_status,
  round,
  time,
  method,
  method_type,
  bout_weight,
  url,
  last_updated_at,
  clinch_time,
  ground_time,
  standing_time,
  r_knockdowns,
  b_knockdowns,
  r_takedowns_landed,
  b_takedowns_landed,
  r_takedowns_attempted,
  b_takedowns_attempted,
  r_sig_strikes_landed,
  b_sig_strikes_landed,
  r_sig_strikes_attempted,
  b_sig_strikes_attempted,
  r_sig_strikes_accuracy,
  b_sig_strikes_accuracy,
  r_total_strikes_landed,
  b_total_strikes_landed,
  r_total_strikes_attempted,
  b_total_strikes_attempted,
  r_submissions_attempted,
  b_submissions_attempted,
  r_control_time,
  b_control_time,
  r_clinch_control_time,
  b_clinch_control_time,
  r_ground_control_time,
  b_ground_control_time
FROM
  {{ ref('int_fights_transformations') }}
