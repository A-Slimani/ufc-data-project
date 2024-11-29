SELECT 
    f1.first_name || ' ' || f1.last_name AS name,
    f1.weight,
    {{ generate_weight_classes('weight') }} AS weight_class,
    f1.height,
    f1.reach,
    f1.stance,
    {{ generate_win_percentage('wins', 'losses', 'draws') }} AS win_percentage,
    {{ generate_total_fights('wins', 'losses', 'draws') }} AS total_fights,
    f1.wins,
    f1.losses,
    f1.draws,
    CASE WHEN f2.total_wins_in_ufc_by_dec NOT NULL THEN f2.total_wins_in_ufc_by_unanimous_dec ELSE 0 END , 
    CASE WHEN f2.total_wins_in_ufc_by_unanimous_dec NOT NULL THEN f2.total_wins_in_ufc_by_unanimous_dec ELSE 0 END , 
    CASE WHEN f2.total_wins_in_ufc_by_split_dec NOT NULL THEN f2.total_wins_in_ufc_by_split_dec ELSE 0 END , 
    CASE WHEN f2.total_wins_in_ufc_by_ko_tko NOT NULL THEN f2.total_wins_in_ufc_by_ko_tko ELSE 0 END , 
    CASE WHEN f2.total_wins_in_ufc_by_sub NOT NULL THEN f2.total_wins_in_ufc_by_sub ELSE 0 END , 
FROM 
    {{ source('ufcdb', 'fighters') }} f1
LEFT JOIN 
    {{ ref('fighter_wins_type') }} f2
ON 
    (f1.first_name || ' ' || f1.last_name) = f2.r_fighter