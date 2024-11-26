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
    draws
FROM 
    {{ source('ufcdb', 'fighters') }}
LEFT JOIN 
    {{ source('ufcdb', 'fights') }}
ON
    fighter