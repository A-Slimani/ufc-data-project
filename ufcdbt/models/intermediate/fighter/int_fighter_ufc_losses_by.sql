WITH winning_fighter AS (
  SELECT
    method_type,
    CASE
      WHEN r_fighter_status = 'Loss' THEN r_fighter_id 
      WHEN b_fighter_status = 'Loss' THEN b_fighter_id
      ElSE NULL 
    END AS "fighter_id"
  FROM {{ ref('stg_fights')}}
), counts AS (
  SELECT 
    a.fighter_id,
    COUNT(method_type) AS "ufc_losses",
    COUNT(CASE WHEN a.method_type=1 THEN 1 END) AS "ufc_losses_by_ko_tko", 
    COUNT(CASE WHEN a.method_type=2 THEN 1 END) AS "ufc_losses_by_sub", 
    COUNT(CASE WHEN a.method_type=3 THEN 1 END) AS "ufc_losses_by_dec" 
  FROM winning_fighter a
  JOIN {{ ref('stg_fighters') }} b
  ON a.fighter_id = b.id
  WHERE a.fighter_id IS NOT NULL
  GROUP BY a.fighter_id
)
SELECT
  fighter_id,
  ufc_losses,
  ufc_losses_by_ko_tko,
  {{ get_percentage(['ufc_losses_by_ko_tko', 'ufc_losses']) }} AS "ufc_loss_percentage_by_ko_tko", 
  ufc_losses_by_sub,
  {{ get_percentage(['ufc_losses_by_sub', 'ufc_losses']) }} AS "ufc_loss_percentage_by_sub", 
  ufc_losses_by_dec,
  {{ get_percentage(['ufc_losses_by_dec', 'ufc_losses']) }} AS "ufc_loss_percentage_by_dec" 
FROM counts