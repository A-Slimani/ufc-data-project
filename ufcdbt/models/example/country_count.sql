SELECT
    country,
    COUNT(country) AS "city_count"
FROM
    {{ source('ufcdb', 'events') }}
GROUP BY country