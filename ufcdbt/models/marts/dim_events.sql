SELECT
  id,
  name,
  date,
  city,
  state,
  country,
  venue
FROM
  {{ ref('stg_events') }}