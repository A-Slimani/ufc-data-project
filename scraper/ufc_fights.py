from extensions.missing_pages import get_missing_page_list
from extensions.missing_pages import write_to_file
import psycopg2
import logging
import asyncio
import asyncpg
import hishel
import random
import json
import sys
import os

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler(f"{os.getenv('LOG_DIR')}/ufc_fights.log"), logging.StreamHandler()],
    level=logging.INFO
)

hisel_logger = logging.getLogger("hishel") 
logger = logging.getLogger(__name__)

missing_ids = []

async def get_fight_data(page, semaphore, pool, sleep_time):
  async with semaphore:
    try:
      await asyncio.sleep(sleep_time)
      url = f"https://d29dxerjsp82wz.cloudfront.net/api/v3/fight/live/{page}.json"
      async with hishel.AsyncCacheClient(
        storage=hishel.AsyncFileStorage(base_path="./.cache/ufc_fights/", ttl=3600 * 24 * 7),
        verify=False,
      ) as client:
        try:
          res = await client.get(url, extensions={"force_cache": True})
          if res.status_code != 200:
            logger.error(f"ERROR at page {page}: HTTP ERROR -- {res.status_code}")
            return
        except Exception as e:
          logger.error(f"ERROR at page {page}: {e}")
          return
        
        json_data = res.json()
        fight = json_data["LiveFightDetail"]
        if fight:
          id = fight["FightId"]
          event_id = fight["Event"]["EventId"] # foreign key
          r_fighter_id = fight["Fighters"][0]["FighterId"] # foreign key
          b_fighter_id = fight["Fighters"][1]["FighterId"] # foreign key
          r_fighter_status = fight["Fighters"][0]["Outcome"]["Outcome"]
          b_fighter_status = fight["Fighters"][1]["Outcome"]["Outcome"]
          round = fight["Result"]["EndingRound"]
          time = fight["Result"]["EndingTime"]
          method = fight["Result"]["Method"]
          bout_weight = fight["WeightClass"]["Description"]
          url_link = url
          start_time = fight["Event"]["StartTime"]
          fight_stats = fight["FightStats"]
          if fight_stats:
            r_fight_stats = json.dumps(fight["FightStats"][0])
            b_fight_stats = json.dumps(fight["FightStats"][1])
          else:
            logger.info(f"no fight stats found for id {page}")
            return

          async with pool.acquire() as conn:
            await conn.execute(
              """
              INSERT INTO raw_fights (
                id, event_id, start_time, r_fighter_id, b_fighter_id, 
                r_fighter_status, b_fighter_status, round, time, 
                method, bout_weight, r_fight_stats, b_fight_stats, url, last_updated_at
              ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, CURRENT_TIMESTAMP)
              ON CONFLICT (id) DO UPDATE SET
                event_id = EXCLUDED.event_id,
                start_time = EXCLUDED.start_time,
                r_fighter_id = EXCLUDED.r_fighter_id,
                b_fighter_id = EXCLUDED.b_fighter_id,
                r_fighter_status = EXCLUDED.r_fighter_status,
                b_fighter_status = EXCLUDED.b_fighter_status,
                round = EXCLUDED.round,
                time = EXCLUDED.time,
                method = EXCLUDED.method,
                bout_weight = EXCLUDED.bout_weight,
                r_fight_stats = EXCLUDED.r_fight_stats,
                b_fight_stats = EXCLUDED.b_fight_stats,
                url = EXCLUDED.url,
                last_updated_at = CURRENT_TIMESTAMP
              """,
              id, event_id, start_time, r_fighter_id, b_fighter_id,
              r_fighter_status, b_fighter_status, round, time, 
              method, bout_weight, r_fight_stats, b_fight_stats, url_link
              )
        else:
          logger.info(f"No data found for page {page}")
          missing_ids.append(page)
          pass

    except Exception as e:
      logger.error(f'Error fetching data for page {page}: {str(e)}')
      raise
       

def create_fight_table():    
  conn = psycopg2.connect(os.getenv("DB_URI"))
  cursor = conn.cursor()
  cursor.execute(
  """
  CREATE TABLE IF NOT EXISTS raw_fights (
    id INTEGER PRIMARY KEY,
    event_id INTEGER REFERENCES raw_events(id) ON DELETE CASCADE,
    start_time TEXT,
    r_fighter_id INTEGER REFERENCES raw_fighters(id) ON DELETE CASCADE,
    r_fighter_status TEXT,
    b_fighter_id INTEGER REFERENCES raw_fighters(id) ON DELETE CASCADE,
    b_fighter_status TEXT,
    round INTEGER,
    time TEXT,
    method TEXT,
    bout_weight TEXT,
    r_fight_stats JSONB,
    b_fight_stats JSONB,
    url TEXT,
    last_updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
  )
  """
  )
  conn.commit()
  cursor.close()
  conn.close()

def update_recently_completed_fights():
  conn = psycopg2.connect(os.getenv("DB_URI"))
  with conn.cursor() as cursor:
    cursor.execute("""
    SELECT f.id 
    FROM raw_events e
    WHERE e.date::date > CURRENT_DATE - 1
    LEFT JOIN raw_fights f
    ON e.id = f.event_id
    """)
  pass

async def main():
  create_fight_table()

  pool = await asyncpg.create_pool(
    os.getenv("DB_URI"),
    min_size=1,
    max_size=16
  )

  semaphore = asyncio.Semaphore(32)
  if sys.argv[1] == "--missing":
    tasks = [get_fight_data(i, semaphore, pool, 1) for i in range(30, 11500)]
  elif sys.argv[1] == "--update": # TO UPDATE
    tasks = [get_fight_data(i, semaphore, pool, 1) for i in range(30, 11500)]
  elif sys.argv[1] == "--build":
    tasks = [get_fight_data(i, semaphore, pool, 1) for i in range(30, 11500)]
  elif sys.argv[1] == "--test":
    random_pages = [random.randint(100, 10000) for _ in range(40)]
    tasks = [get_fight_data(page, semaphore, pool, 1) for page in random_pages]
  else:
    print("Need to pass an argument: --partial, --recent, --build, --test")
    
  await asyncio.gather(*tasks)
  write_to_file(f"{os.getenv('LOG_DIR')}/missing_fights.txt", missing_ids)
  
if __name__ == '__main__':
  asyncio.run(main())  