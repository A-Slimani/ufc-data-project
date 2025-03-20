import psycopg2
import logging
import asyncio
import asyncpg
import hishel
import os

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler('ufc_fighters.log'), logging.StreamHandler()],
    level=logging.DEBUG,
)

hishel_logger = logging.getLogger("hishel")
httpx_logger = logging.getLogger("httpx")
hishel_logger.setLevel(logging.DEBUG)
httpx_logger.setLevel(logging.DEBUG)

logger = logging.getLogger(__name__)


async def get_fighter_data(page, semaphore, pool): 
  async with semaphore:
    try:
      async with hishel.AsyncCacheClient(
        storage=hishel.AsyncFileStorage(base_path="./.cache/ufc_events/", ttl=3600 * 24),
        verify=False,
      ) as client:
        try:
          res = await client.get(
            f"https://d29dxerjsp82wz.cloudfront.net/api/v3/event/live/{page}.json",
            extensions={"force_cache": True},
          )    
          if res.status_code != 200:
            logger.error(f"Error fetching data for page {page}: HTTP ERROR -- {res.status_code}")
            return
        except Exception as e:
          logger.error(f"Error fetching data for page {page}: {str(e)}")
          return

        json_data = res.json()
        event_details = json_data["LiveEventDetail"]          

        if event_details:
          for fight in event_details["FightCard"]: 
            for fighter in fight["Fighters"]:
              fighter_data = {
                "id": fighter["FighterId"],
                "first_name": fighter["Name"]["FirstName"],
                "last_name": fighter["Name"]["LastName"], 
                "nickname": fighter["Name"]["NickName"],
                "hometown_city": fighter["Born"]["City"],
                "hometown_state": fighter["Born"]["State"],
                "hometown_country": fighter["Born"]["Country"],
                "trains_at_city": fighter["FightingOutOf"]["City"],
                "trains_at_state": fighter["FightingOutOf"]["State"],
                "trains_at_country": fighter["FightingOutOf"]["Country"],
                "wins": fighter["Record"]["Wins"],
                "losses": fighter["Record"]["Losses"],
                "draws": fighter["Record"]["Draws"],
                "age": fighter["Age"],
                "height": fighter["Height"],
                "stance": fighter["Stance"],
                "reach": fighter["Reach"],
                "weight_class": fighter["Weight"],
                "url": fighter["UFCLink"],
              }
        
              async with pool.acquire() as conn:
                await conn.execute(
                  """
                  INSERT INTO fighters (
                    id, first_name, last_name, 
                    nickname, hometown_city, hometown_state, 
                    hometown_country, trains_at_city, trains_at_state, 
                    trains_at_country, wins, losses, draws, age, height, 
                    stance, reach, weight_class, url, last_updated_at
                  ) VALUES (
                    $1, $2, $3, $4, $5, 
                    $6, $7, $8, $9, $10, 
                    $11, $12, $13, $14, $15, 
                    $16, $17, $18, $19, CURRENT_TIMESTAMP
                  )
                  ON CONFLICT (id) DO UPDATE SET
                    id = EXCLUDED.id,
                    first_name = EXCLUDED.first_name,
                    last_name = EXCLUDED.last_name,
                    nickname = EXCLUDED.nickname,
                    hometown_city = EXCLUDED.hometown_city,
                    hometown_state = EXCLUDED.hometown_state,
                    hometown_country = EXCLUDED.hometown_country,
                    trains_at_city = EXCLUDED.trains_at_city,
                    trains_at_state = EXCLUDED.trains_at_state,
                    trains_at_country = EXCLUDED.trains_at_country,
                    wins = EXCLUDED.wins,
                    losses = EXCLUDED.losses,
                    draws = EXCLUDED.draws,
                    age = EXCLUDED.age,
                    height = EXCLUDED.height,
                    stance = EXCLUDED.stance,
                    reach = EXCLUDED.reach,
                    weight_class = EXCLUDED.weight_class,
                    url = EXCLUDED.url,
                    last_updated_at = CURRENT_TIMESTAMP
                  """,
                  fighter_data["id"],
                  fighter_data["first_name"],
                  fighter_data["last_name"],
                  fighter_data["nickname"],
                  fighter_data["hometown_city"],
                  fighter_data["hometown_state"],
                  fighter_data["hometown_country"],
                  fighter_data["trains_at_city"],
                  fighter_data["trains_at_state"],
                  fighter_data["trains_at_country"],
                  fighter_data["wins"],
                  fighter_data["losses"],
                  fighter_data["draws"],
                  fighter_data["age"],
                  fighter_data["height"],
                  fighter_data["stance"],
                  fighter_data["reach"],
                  fighter_data["weight_class"],
                  fighter_data["url"],
                )
        else:
          logger.info(f"No data found for page {page}")
          pass

    except Exception as e:
      logger.error(f"Error fetching data for page {page}: {str(e)}") 
      raise
    
def create_fighter_table():
  conn = psycopg2.connect(os.getenv("DB_URI")) 
  cursor = conn.cursor()
  cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS fighters (
      id INTEGER PRIMARY KEY,
      first_name TEXT,
      last_name TEXT,
      nickname TEXT,
      hometown_city TEXT,
      hometown_state TEXT,
      hometown_country TEXT,
      trains_at_city TEXT,
      trains_at_state TEXT,
      trains_at_country TEXT,
      wins INTEGER,
      losses INTEGER,
      draws INTEGER,
      age INTEGER,
      height INTEGER,
      stance TEXT,
      reach INTEGER,
      weight_class INTEGER, 
      url TEXT,
      last_updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
    )
    """
  )
  conn.commit()
  cursor.close()
  conn.close()

async def main():
  create_fighter_table()

  pool = await asyncpg.create_pool(
    os.getenv("DB_URI"),
    min_size=1,
    max_size=16
  )

  semaphore = asyncio.Semaphore(16)
  tasks = [get_fighter_data(i, semaphore, pool) for i in range(1, 1300)]
  await asyncio.gather(*tasks)

if __name__ == '__main__':
  asyncio.run(main())