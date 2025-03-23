SELECT
  id,
  first_name,
  last_name,

  {{ }} 
FROM
  {{ source('ufcdb', 'fighters')}}