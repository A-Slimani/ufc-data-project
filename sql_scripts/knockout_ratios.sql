-- total ko/tko ratio
WITH counts AS (
    SELECT
        bout_weight,
        COUNT(CASE WHEN method='KO/TKO' THEN 1 END) as "ko_tko_wins",
        COUNT(method) as "all_fights"
    FROM dbt_schema.fact_fights
    GROUP BY bout_weight
)
SELECT
    bout_weight,
    ko_tko_wins,
    all_fights,
    ROUND(KO_TKO_wins::NUMERIC / all_fights, 2) * 100 AS "ko_tko_ratio"
FROM counts
WHERE all_fights > 150
ORDER BY "ko_ratio" DESC

-- ko / tko ratio over time
WITH counts_per_year AS (
    SELECT
        bout_weight,
        EXTRACT(YEAR FROM fight_date) as fight_year,
        COUNT(CASE WHEN method='KO/TKO' THEN 1 END) as "ko_tko_wins",
        COUNT(fight_date) AS fights_in_the_year
    FROM dbt_schema.fact_fights
    GROUP BY bout_weight, fight_year HAVING COUNT(fight_date) > 10
)
SELECT  
    bout_weight,
    fight_year,
    ko_tko_wins,
    fights_in_the_year,
    ROUND(ko_tko_wins::NUMERIC / fights_in_the_year, 2) * 100 AS "ko_tko_ratio" 
FROM counts_per_year 
WHERE fight_year > 2005 
ORDER BY bout_weight, fight_year