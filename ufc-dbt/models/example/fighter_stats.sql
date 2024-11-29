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
    f2.total_wins_by_dec,
    f2.total_wins_by_unanimous_dec,
    f2.total_wins_by_split_dec,
    f2.total_wins_by_ko_tko,
    f2.total_wins_by_sub
FROM 
    {{ source('ufcdb', 'fighters') }} f1
LEFT JOIN 
    {{ ref('fighter_wins_type') }} f2
ON 
    (f1.first_name || ' ' || f1.last_name) = f2.r_fighter