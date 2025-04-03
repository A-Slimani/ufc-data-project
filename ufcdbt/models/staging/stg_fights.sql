SELECT
  f.id,
  f.event_id,
  f.r_fighter_id,
  f.r_fighter_status,
  f.b_fighter_id,
  f.b_fighter_status,
  f.round,
  f.time,
  f.method,
  {{ win_type_ratio('f.method') }} AS "method_type",
  f.bout_weight,
  f.url,
  f.last_updated_at,
  f.r_fight_stats->>'ClinchTime' AS clinch_time,
  f.r_fight_stats->>'GroundTime' AS ground_time,
  f.r_fight_stats->>'StandingTime' AS standing_time,
  (f.r_fight_stats->>'Knockdowns')::NUMERIC AS r_knockdowns,
  (f.b_fight_stats->>'Knockdowns')::NUMERIC AS b_knockdowns,
  (f.r_fight_stats->>'TakedownsLanded')::NUMERIC AS r_takedowns_landed,
  (f.b_fight_stats->>'TakedownsLanded')::NUMERIC AS b_takedowns_landed,
  (f.r_fight_stats->>'TakedownsAttempted')::NUMERIC AS r_takedowns_attempted,
  (f.b_fight_stats->>'TakedownsAttempted')::NUMERIC AS b_takedowns_attempted,
  (f.r_fight_stats->>'SigStrikesLanded')::NUMERIC AS r_sig_strikes_landed,
  (f.b_fight_stats->>'SigStrikesLanded')::NUMERIC AS b_sig_strikes_landed,
  (f.r_fight_stats->>'SigStrikesAttempted')::NUMERIC AS r_sig_strikes_attempted,
  (f.b_fight_stats->>'SigStrikesAttempted')::NUMERIC AS b_sig_strikes_attempted,
  (f.r_fight_stats->>'SigStrikesAccuracy')::NUMERIC AS r_sig_strikes_accuracy,
  (f.b_fight_stats->>'SigStrikesAccuracy')::NUMERIC AS b_sig_strikes_accuracy,
  (f.r_fight_stats->>'TotalStrikesLanded')::NUMERIC AS r_total_strikes_landed,
  (f.b_fight_stats->>'TotalStrikesLanded')::NUMERIC AS b_total_strikes_landed,
  (f.r_fight_stats->>'TotalStrikesAttempted')::NUMERIC AS r_total_strikes_attempted,
  (f.b_fight_stats->>'TotalStrikesAttempted')::NUMERIC AS b_total_strikes_attempted,
  (f.r_fight_stats->>'SubmissionsAttempted')::NUMERIC AS r_submissions_attempted,
  (f.b_fight_stats->>'SubmissionsAttempted')::NUMERIC AS b_submissions_attempted,
  f.r_fight_stats->>'ControlTime' AS r_control_time,
  f.b_fight_stats->>'ControlTime' AS b_control_time,
  f.r_fight_stats->>'ClinchControlTime' AS r_clinch_control_time,
  f.b_fight_stats->>'ClinchControlTime' AS b_clinch_control_time,
  f.r_fight_stats->>'GroundControlTime' AS r_ground_control_time,
  f.b_fight_stats->>'GroundControlTime' AS b_ground_control_time
FROM
  {{ source('database', 'raw_fights') }} f
JOIN
  {{ ref('stg_events') }} e
ON
  f.event_id = e.id

