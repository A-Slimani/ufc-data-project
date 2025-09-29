from extensions.missing_pages import get_missing_page_list
from extensions.missing_pages import write_to_file
from pathlib import Path
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
        storage=hishel.AsyncFileStorage(base_path=Path("./.cache/ufc_fights/"), ttl=3600 * 24 * 7),
        verify=False,
      ) as client:
        try:
          res = await client.get(url, extensions={"force_cache": True})
          if res.status_code != 200:
            logger.error(f"ERROR at page {page}: HTTP ERROR -- {res.status_code}")
            return (False, f"HTTP ERROR, {page}")
        except Exception as e:
          logger.error(f"ERROR at page {page}: {e}")
          return (False, f"Page Error {page}")
        
        json_data = res.json()
        fight = json_data["LiveFightDetail"]
        if fight:
          id = fight["FightId"]
          event_id = fight["Event"]["EventId"] # foreign key
          r_fighter_id = fight["Fighters"][0]["FighterId"] # foreign key
          b_fighter_id = fight["Fighters"][1]["FighterId"] # foreign key
          r_fighter_status = fight["Fighters"][0]["Outcome"]["Outcome"]
          b_fighter_status = fight["Fighters"][1]["Outcome"]["Outcome"]
          fight_order = fight["FightOrder"]
          ending_round = fight["Result"]["EndingRound"]
          time = fight["Result"]["EndingTime"]
          method = fight["Result"]["Method"]
          bout_weight = fight["WeightClass"]["Description"]
          bout_rounds = fight["RuleSet"]["PossibleRounds"]
          url_link = url
          start_time = fight["Event"]["StartTime"]
          fight_stats = fight["FightStats"]
          if fight_stats:
            r_fight_stats = json.dumps(fight["FightStats"][0])
            b_fight_stats = json.dumps(fight["FightStats"][1])
          else:
            r_fight_stats = None
            b_fight_stats = None
            logger.info(f"no fight stats found for id {page}")

          async with pool.acquire() as conn:
            await conn.execute(
              """
              INSERT INTO raw_fights (
                id, event_id, start_time, r_fighter_id, b_fighter_id, 
                r_fighter_status, b_fighter_status, fight_order, ending_round, time, 
                method, bout_weight, bout_rounds, r_fight_stats, b_fight_stats, url, last_updated_at
              ) VALUES ($1, $2, $3, $4, $5, $6, $7, 
                $8, $9, $10, $11, $12, $13, $14, $15, $16, CURRENT_TIMESTAMP
              )
              ON CONFLICT (id) DO UPDATE SET
                event_id = EXCLUDED.event_id,
                start_time = EXCLUDED.start_time,
                r_fighter_id = EXCLUDED.r_fighter_id,
                b_fighter_id = EXCLUDED.b_fighter_id,
                r_fighter_status = EXCLUDED.r_fighter_status,
                b_fighter_status = EXCLUDED.b_fighter_status,
                fight_order = EXCLUDED.fight_order,
                ending_round = EXCLUDED.ending_round,
                time = EXCLUDED.time,
                method = EXCLUDED.method,
                bout_weight = EXCLUDED.bout_weight,
                bout_rounds = EXCLUDED.bout_rounds,
                r_fight_stats = EXCLUDED.r_fight_stats,
                b_fight_stats = EXCLUDED.b_fight_stats,
                url = EXCLUDED.url,
                last_updated_at = CURRENT_TIMESTAMP
              """,
              id, event_id, start_time, r_fighter_id, b_fighter_id,
              r_fighter_status, b_fighter_status, fight_order, ending_round, time, 
              method, bout_weight, bout_rounds, r_fight_stats, b_fight_stats, url_link
              )
          return (True, "Success")
        else:
          logger.info(f"No data found for page {page}")
          missing_ids.append(page)
          return (False, f"No fight data found ERROR {page}")

    except Exception as e:
      logger.error(f'Error fetching data for page {page}: {str(e)}')
      return (False, f"Error fetching data for page {page}")
       

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
    fight_order INTEGER,
    ending_round INTEGER,
    time TEXT,
    method TEXT,
    bout_weight TEXT,
    bout_rounds INTEGER,
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


def get_recent_fights(date_from: int):
  conn = psycopg2.connect(os.getenv("DB_URI"))
  with conn.cursor() as cursor:
    cursor.execute(f"""
    SELECT MIN(id)
    FROM dbt_schema.stg_fights
    WHERE fight_date > CURRENT_DATE - INTERVAL '{date_from} WEEKS'
    """)
    start_page = cursor.fetchone()
    if start_page is not None:
      return start_page[0]
    else:
      logger.error("No records found in the database." \
        "Pick a valid date or check the database")
      raise


async def process_tasks(tasks):
  success_count = 0
  consecutive_fail_count = 0
  fail_threshold = 20
  try:
    for future in asyncio.as_completed(tasks):
      try:
        result = await future
        if result[0]:
          success_count += 1
          consecutive_fail_count = 0
        else:
          print(result[1])
          consecutive_fail_count += 1

        if consecutive_fail_count > fail_threshold:
          logger.warning(f"Reached fail threshold of {fail_threshold}, stopping all tasks...")
          for task in tasks:
            if not task.done():
              task.cancel()
          break
        logger.info(f"Success Count: {success_count}, Consecutive Fail Count: {consecutive_fail_count}")

      except asyncio.CancelledError:
        logger.info("Task was cancelled")
        continue
        
  finally:
    await asyncio.gather(*tasks, return_exceptions=True)

async def main():
  create_fight_table()

  pool = await asyncpg.create_pool(
    os.getenv("DB_URI"),
    min_size=1,
    max_size=16
  )

  semaphore = asyncio.Semaphore(32)
  pages = []
  if sys.argv[1] == "--missing":
    pages = get_missing_page_list(f"{os.getenv('LOG_DIR')}/missing_fights.txt")
  elif sys.argv[1] == "--recent": 
    try:
      weeks_from = int(sys.argv[2])
      if weeks_from > 52:
        print("Argument value too large. Consider using --build function")
      elif weeks_from < 1:
        print("Invalid number. Please input a number between 1 to 52")
      else:
        pages = range(get_recent_fights(weeks_from), 100_000) 
    except IndexError:
        print("No Argument passed default to updating from 4 weeks ago...")
        pages = range(get_recent_fights(4), 100_000)
    except ValueError:
      print("Invalid argument. Please input a number")
      raise
  elif sys.argv[1] == "--build":
    pages = range(30, 100_000) #Need to find a better way than just hard coding 100_000 will eventually cap
  elif sys.argv[1] == "--test":
    pages = [random.randint(12_000, 15_000) for _ in range(50)]
  elif sys.argv[1] == "--help":
    print("Usage: python ufc_fighters_and_events.py --missing | --recent | --build | --test")
    print("  --missing: Get missing pages from the list")
    print("  --recent: Get recent and upcoming events")
    print("  --build: Build the database from scratch")
    print("  --test: Get random pages for testing")
    print("  --help: Show this help message")
  else:
    print("Need to pass an argument: --missing, --recent, --full, --test")
  
  tasks = [asyncio.create_task(get_fight_data(page, semaphore, pool, 1)) for page in pages]

  await process_tasks(tasks)

  write_to_file(f"{os.getenv('LOG_DIR')}/missing_fights.txt", missing_ids)
  
if __name__ == '__main__':
  asyncio.run(main())  
