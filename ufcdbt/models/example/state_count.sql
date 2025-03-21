SELECT
    "state",
    COUNT("state") AS "city_count"
FROM
    {{ source('ufcdb', 'events') }}
GROUP BY "state"