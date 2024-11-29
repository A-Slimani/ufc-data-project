SELECT 
    first_name || ' ' || last_name AS fighter_name,
    weight,
    {{ generate_weight_classes('weight') }} AS weight_class,
    height,
    reach,
    stance,
    {{ generate_win_percentage('wins', 'losses', 'draws') }} AS win_percentage,
    {{ generate_total_fights('wins', 'losses', 'draws') }} AS total_fights,
    wins,
    losses,
    draws,
    {{ generate_wins_by_type('method') }}
FROM 
    {{ source('ufcdb', 'fighters') }} f1
LEFT JOIN
    {{ source('ufcdb', 'fights') }} f2
ON
    (f1.first_name || ' ' || f1.last_name) = f2.r_fighter