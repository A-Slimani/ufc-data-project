CREATE TABLE IF NOT EXISTS country_codes (
  id SERIAL PRIMARY KEY,
  name TEXT,
  area TEXT,
  cioc TEXT,
  cca2 TEXT,
  capital TEXT,
  lat TEXT,
  lng TEXT,
  cca3 TEXT
)