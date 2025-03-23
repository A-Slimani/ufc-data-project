SELECT
    "state",
    COUNT("state") AS "state_count"
FROM
    {{ source('ufcdb', 'events') }}
GROUP BY "state"