select
	r_fighter_id as "id",
	r_fighter_name as "name",
	fight_date 
from dbt_schema.fact_fights
where
	fight_date < CURRENT_DATE
	and
	fight_date > CURRENT_DATE - INTERVAL'3 years'
	and
	r_fighter_status is not null
union
select
	b_fighter_id as "id",
	b_fighter_name as "name",
	fight_date
from dbt_schema.fact_fights
where 
	fight_date < CURRENT_DATE
	and
	fight_date > CURRENT_DATE - INTERVAL'3 years'
	and
	b_fighter_status is not null
order by fight_date 