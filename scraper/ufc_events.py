from datetime import datetime
import requests_cache
import requests
import psycopg2
import os

'''
TODO
  - Transform data to fit db schema
    - Use previous code
  - Store data in db
  - Create functionality to loop through all events
'''

requests_cache.install_cache('ufc_cache', use_cache_dir=True, expire_after=60 * 60 * 24) # Expire after 24 hours
res = requests.get("https://d29dxerjsp82wz.cloudfront.net/api/v3/event/live/100.json")

json_data = res.json()
event_details = json_data['LiveEventDetail']

date = datetime.fromisoformat(event_details['StartTime'])

event_data = {
  'id': event_details['EventId'],
  'name': event_details['Name'],
  'date': date, 
  'city': event_details['Location']['City'],
  'state': event_details['Location']['State'],
  'country': event_details['Location']['Country'],
  'venue': event_details['Location']['Venue']
}

print(event_data)

# On inital script run
conn = psycopg2.connect(os.getenv("DB_URI"))
cursor = conn.cursor()
cursor.execute(
  """
  CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY, 
    name TEXT,
    date TEXT,
    city TEXT,
    state TEXT,
    country TEXT,
    venue TEXT,
    last_updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
  ) 
  """
)
conn.commit()
