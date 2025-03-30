SELECT
  id,
  name,
  date,
  city,
  state,
  country,
  venue,
  last_updated_at
FROM
  {{ source('ufcdb', 'raw_events') }}
WHERE 
  name LIKE 'UFC%' OR name LIKE 'The Ultimate%'
  