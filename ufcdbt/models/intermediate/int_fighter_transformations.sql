SELECT 
  p.fighter_id,
  f.first_name,
  f.last_name,
  f.nick_name,
  f.hometown_city,
  f.hometown_state,
  f.hometown_country,
  f.hometown_country_tricode,
  f.trains_at_city,
  f.trains_at_state,
  f.trains_at_country,
  f.trains_at_country_tricode,
  (f.wins + f.losses + f.draws) AS "total_fights",
  f.wins AS "total_wins",
  f.losses AS "total_losses",
  f.draws AS "total_draws",
  {{ get_percentage(['f.wins', 'f.losses', 'f.draws']) }} AS "total_win_percentage",
  p.ufc_fights,
  p.ufc_wins,
  p.ufc_losses,
  p.ufc_draws,
  p.ufc_win_percentage,
  b.ko_tko AS "wins_by_ko_tko",
  b.dec AS "wins_by_dec",
  b.sub AS "wins_by_sub",
  fs.career_knockdowns,
  fs.career_takedowns_attempted,
  fs.career_takedowns_landed,
  fs.career_takedown_accuracy,
  fs.career_sig_strikes_attempted,
  fs.career_sig_strikes_landed,
  fs.career_sig_strike_accuracy,
  fs.career_total_strikes_attempted,
  fs.career_total_strikes_landed,
  fs.career_total_strike_accuracy,
  fs.career_submissions_attempted,
  fs.career_control_time_seconds,
  fs.career_clinch_control_time_seconds,
  fs.career_ground_control_time_seconds
FROM {{ ref('int_fighter_percentages') }} p
JOIN 
  {{ ref('int_fighter_wins_by') }} b ON p.fighter_id = b.fighter_id
JOIN
  {{ ref('stg_fighters') }} f ON f.id = b.fighter_id
JOIN 
  {{ ref('int_fighter_fight_stats') }} fs ON fs.fighter_id = f.id 