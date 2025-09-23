-- total amount
SELECT
    full_name,
    ufc_wins_by_sub,
    ufc_wins,
    total_fights
FROM dbt_schema.dim_fighters
WHERE last_active > CURRENT_DATE - INTERVAL '2 years'
ORDER BY ufc_wins_by_sub DESC
LIMIT 10

-- highest ratio
-- ratio of wins / sub
SELECT
    full_name,
    ufc_wins_by_sub,
    ufc_fights,
    ROUND(ufc_wins_by_sub::NUMERIC / ufc_wins, 2) AS "win_sub_ratio"
FROM dbt_schema.dim_fighters
WHERE ufc_wins >= 5 -- AND last_active > CURRENT_DATE - INTERVAL '2 years'
ORDER BY win_sub_ratio DESC
LIMIT 10

-- ration of fights / sub
SELECT
    full_name,
    ufc_wins_by_sub,
    ufc_fights,
    ROUND(ufc_wins_by_sub::NUMERIC / ufc_fights, 2) AS "fight_sub_ratio"
FROM dbt_schema.dim_fighters
WHERE ufc_wins >= 5 -- AND last_active > CURRENT_DATE - INTERVAL '2 years'
ORDER BY sub_ratio DESC
LIMIT 10
