WITH combined_records AS (
	SELECT
		r_fighter_id AS "id",
		r_fighter_name AS "name",
		fight_date
	FROM dbt_schema.fact_fights
	UNION
	SELECT
		b_fighter_id AS "id",
		b_fighter_name AS "name",
		fight_date
	FROM dbt_schema.fact_fights
)
SELECT 
	id, 
	name, 
	MAX(fight_date) AS "last_fought" 
FROM combined_records
GROUP BY id, name
ORDER BY MAX(fight_date) DESC