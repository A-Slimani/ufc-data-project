-- removing non ufc values since I will not be using them
DELETE FROM events
WHERE name NOT LIKE 'UFC%' and name NOT LIKE 'THE Ultimate%'
