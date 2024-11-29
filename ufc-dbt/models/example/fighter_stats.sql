SELECT 
    f2.r_fighter,
    weight,
    {{ generate_weight_classes('weight') }} AS weight_class,
    height,
    reach,
    stance,
    {{ generate_win_percentage('wins', 'losses', 'draws') }} AS win_percentage,
    {{ generate_total_fights('wins', 'losses', 'draws') }} AS total_fights,
    wins,
    losses,
    draws
FROM 
    {{ source('ufcdb', 'fighters') }} f1
LEFT JOIN 
    {{ generate_wins_by_type() }} f2
ON 
    (f1.first_name || ' ' || f1.last_name) = f2.r_fighter