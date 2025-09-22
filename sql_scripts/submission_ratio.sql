-- total amount
SELECT
    full_name,
    ufc_wins_by_sub
FROM dbt_schema.dim_fighters
ORDER BY ufc_wins_by_sub DESC
LIMIT 10

-- highest ratio
SELECT
    full_name,
    ufc_wins_by_sub,
    ufc_wins,
    ROUND(ufc_wins_by_sub / ufc_wins, 2) AS "sub_ratio"
FROM dbt_schema.dim_fighters
WHERE ufc_wins >= 5
ORDER BY