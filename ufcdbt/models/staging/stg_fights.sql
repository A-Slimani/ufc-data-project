SELECT
  f.id,
  f.event_id,
  f.r_fighter_id,
  f.r_fighter_status,
  f.b_fighter_id,
  f.b_fighter_status,
  f.fight_order,
  f.ending_round,
  f.time,
  f.method,
  {{ fight_result_type('f.method') }} AS "method_type",
  f.bout_weight,
  {{ generate_weight_class_id('f.bout_weight') }} AS "bout_weight_id",
  {{ bout_rounds_conversion('f.bout_rounds') }} AS "bout_rounds",
  f.url,
  f.start_time::timestamp::date AS "fight_date",
  f.last_updated_at,
  f.r_fight_stats->>'ClinchTime' AS clinch_time,
  f.r_fight_stats->>'GroundTime' AS ground_time,
  f.r_fight_stats->>'StandingTime' AS standing_time,
  (f.r_fight_stats->>'Knockdowns')::INT AS r_knockdowns,
  (f.b_fight_stats->>'Knockdowns')::INT AS b_knockdowns,
  (f.r_fight_stats->>'TakedownsLanded')::INT AS r_takedowns_landed,
  (f.b_fight_stats->>'TakedownsLanded')::INT AS b_takedowns_landed,
  (f.r_fight_stats->>'TakedownsAttempted')::INT AS r_takedowns_attempted,
  (f.b_fight_stats->>'TakedownsAttempted')::INT AS b_takedowns_attempted,
  (f.r_fight_stats->>'SigStrikesLanded')::INT AS r_sig_strikes_landed,
  (f.b_fight_stats->>'SigStrikesLanded')::INT AS b_sig_strikes_landed,
  (f.r_fight_stats->>'SigStrikesAttempted')::INT AS r_sig_strikes_attempted,
  (f.b_fight_stats->>'SigStrikesAttempted')::INT AS b_sig_strikes_attempted,
  COALESCE((f.r_fight_stats->>'SigStrikesAccuracy')::NUMERIC, 0) AS r_sig_strikes_accuracy,
  COALESCE((f.b_fight_stats->>'SigStrikesAccuracy')::NUMERIC, 0) AS b_sig_strikes_accuracy,
  (f.r_fight_stats->>'TotalStrikesLanded')::INT AS r_total_strikes_landed,
  (f.b_fight_stats->>'TotalStrikesLanded')::INT AS b_total_strikes_landed,
  (f.r_fight_stats->>'TotalStrikesAttempted')::INT AS r_total_strikes_attempted,
  (f.b_fight_stats->>'TotalStrikesAttempted')::INT AS b_total_strikes_attempted,
  (f.r_fight_stats->>'SubmissionsAttempted')::INT AS r_submissions_attempted,
  (f.b_fight_stats->>'SubmissionsAttempted')::INT AS b_submissions_attempted,
  f.r_fight_stats->>'ControlTime' AS r_total_control_time,
  f.b_fight_stats->>'ControlTime' AS b_total_control_time,
  f.r_fight_stats->>'ClinchControlTime' AS r_clinch_control_time,
  f.b_fight_stats->>'ClinchControlTime' AS b_clinch_control_time,
  f.r_fight_stats->>'GroundControlTime' AS r_ground_control_time,
  f.b_fight_stats->>'GroundControlTime' AS b_ground_control_time
FROM
  {{ source('database', 'raw_fights') }} f
LEFT JOIN
  {{ source('database', 'raw_events') }} e
ON 
  f.event_id = e.id
WHERE
  CAST(organisation_data ->> 'OrganizationId' AS INTEGER) = 1
  AND
  b_fighter_id IS NOT NULL 
  AND 
  r_fighter_id IS NOT NULL
  AND
  b_fighter_status IS NOT NULL
  AND
  r_fighter_status IS NOT NULL
  AND 
  f.start_time::timestamp::date > '2000-01-01'
