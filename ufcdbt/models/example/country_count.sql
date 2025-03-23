SELECT
    country,
    COUNT(country) AS "country_count"
FROM
    {{ source('ufcdb', 'events') }}
GROUP BY country