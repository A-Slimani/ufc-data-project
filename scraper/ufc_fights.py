import psycopg2
import logging
import asyncio
import asyncpg
import hishel
import json
import os

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("ufc_fights.log"), logging.StreamHandler()],
    level=logging.DEBUG
)

hisel_logger = logging.getLogger("hishel") 

logger = logging.getLogger(__name__)

async def get_fight_data(page, semaphore, pool, sleep_time):
  async with semaphore:
    try:
      await asyncio.sleep(sleep_time)
      url = f"https://d29dxerjsp82wz.cloudfront.net/api/v3/fight/live/{page}.json"
      async with hishel.AsyncCacheClient(
        storage=hishel.AsyncFileStorage(base_path="./.cache/ufc_fights/", ttl=3600 * 24),
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
              INSERT INTO fights (
                id, event_id, r_fighter_id, b_fighter_id, 
                r_fighter_status, b_fighter_status, round, time, 
                method, bout_weight, r_fight_stats, b_fight_stats, url, last_updated_at
              ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, CURRENT_TIMESTAMP)
              ON CONFLICT (id) DO UPDATE SET
                event_id = EXCLUDED.event_id,
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
              id, event_id, r_fighter_id, b_fighter_id,
              r_fighter_status, b_fighter_status, round, time, 
              method, bout_weight, r_fight_stats, b_fight_stats, url_link
              )
        else:
          logger.info(f"No data found for page {page}")
          pass

    except Exception as e:
      logger.error(f'Error fetching data for page {page}: {str(e)}')
      raise
       

def create_fight_table():    
  conn = psycopg2.connect(os.getenv("DB_URI"))
  cursor = conn.cursor()
  cursor.execute(
  """
  CREATE TABLE IF NOT EXISTS fights (
    id INTEGER PRIMARY KEY,
    event_id INTEGER REFERENCES events(id) ON DELETE CASCADE,
    r_fighter_id INTEGER REFERENCES fighters(id) ON DELETE CASCADE,
    r_fighter_status TEXT,
    b_fighter_id INTEGER REFERENCES fighters(id) ON DELETE CASCADE,
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

async def main():
  create_fight_table()

  pool = await asyncpg.create_pool(
    os.getenv("DB_URI"),
    min_size=1,
    max_size=16
  )

  semaphore = asyncio.Semaphore(16)
  tasks = [get_fight_data(i, semaphore, pool, 1) for i in range(30, 11500)]
  await asyncio.gather(*tasks)

if __name__ == '__main__':
  asyncio.run(main())  