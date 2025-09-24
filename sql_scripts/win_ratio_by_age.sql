-- count of ages of fighters at the time
WITH combined_records AS (
    SELECT
        r_age AS "age",
        bout_weight,
        r_fighter_status AS "status"
    FROM dbt_schema.fact_fights
    UNION ALL 
    SELECT
        b_age AS "age",
        bout_weight,
        b_fighter_status AS "status"
    FROM dbt_schema.fact_fights
)
SELECT age, bout_weight, COUNT(status) AS "fights" FROM combined_records
WHERE age IS NOT NULL
GROUP BY age, bout_weight
ORDER BY COUNT(status) 

-- win / loss ratio of fights of each age group
WITH combined_records AS (
    SELECT
        r_age AS "age",
        bout_weight,
        r_fighter_status AS "status"
    FROM dbt_schema.fact_fights
    UNION ALL 
    SELECT
        b_age AS "age",
        bout_weight,
        b_fighter_status AS "status"
    FROM dbt_schema.fact_fights
),
win_loss_count AS (
    SELECT 
        age, 
        bout_weight,
        COUNT(CASE WHEN status='Win' THEN 1 END) AS "wins",
        COUNT(CASE WHEN status='Loss' THEN 1 END) AS "losses",
        COUNT(
            CASE 
                WHEN status='Win' THEN 1
                WHEN status='Loss' THEN 1
                ELSE 0
            END
        ) AS "total_fights"
    FROM combined_records
    -- WHERE age >= 21 AND age <= 40
    GROUP BY age, bout_weight
)
SELECT 
    age,
    bout_weight,
    wins,
    losses,
    total_fights,
    ROUND(wins::NUMERIC / total_fights, 2) AS "win_ratio"  
FROM win_loss_count 
WHERE total_fights >= 10
ORDER BY age, bout_weight 