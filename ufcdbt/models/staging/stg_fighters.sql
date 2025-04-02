SELECT
  id,
  first_name,
  last_name,
  nickname AS "nick_name",
  hometown_city,
  hometown_state,
  {{ country_fix('hometown_country') }},
  trains_at_city,
  trains_at_state,
  {{ country_fix('trains_at_country') }},
  wins,
  losses,
  draws,
  age,
  {{ inches_to_cm('height') }},
  stance,
  {{ inches_to_cm('reach') }},
  {{ weight_zero_to_null('weight') }},
  {{ convert_to_weight_division('weight') }},
  url,
  last_updated_at
FROM
  {{ source('database', 'raw_fighters')}}