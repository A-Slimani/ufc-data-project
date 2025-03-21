SELECT
    city,
    COUNT(city) AS "city_count"
FROM
    {{ source('ufcdb', 'events') }}
GROUP BY city