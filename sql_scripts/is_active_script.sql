WITH combined_records AS (
	SELECT
		r_fighter_id AS "id",
		fight_date
	FROM dbt_schema.stg_fights
	UNION ALL
	SELECT
		b_fighter_id AS "id",
		fight_date
	FROM dbt_schema.stg_fights
)
SELECT 
	id, 
	MAX(fight_date) AS "last_active" 
FROM combined_records
GROUP BY id 
ORDER BY MAX(fight_date) DESC