SELECT
  id,
  name,
  date,
  city,
  state,
  country,
  country_tricode,
  venue,
  organisation_data ->> 'OrganizationId' AS organisation_id,
  organisation_data ->> 'Name' AS organisation_name,
  last_updated_at
FROM
  {{ source('database', 'raw_events') }}
WHERE 
  CAST(organisation_data ->> 'OrganizationId' AS INTEGER) = 1
  