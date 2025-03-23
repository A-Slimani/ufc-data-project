-- filtering out non ufc events
-- unsure if I should include road to ufc?
SELECT
  *
FROM
  {{ source('ufcdb', 'events')}}
WHERE
  name LIKE 'UFC%' OR name LIKE 'The Ultimate%'