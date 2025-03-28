from datetime import datetime
import psycopg2
import logging
import asyncio
import asyncpg
import hishel
import os

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("ufc_events.log"), logging.StreamHandler()],
    level=logging.DEBUG 
)
hishel_logger = logging.getLogger("hishel")
logger = logging.getLogger(__name__)

async def get_event_data(page, semaphore, pool, delay):
    async with semaphore:
        try:
            storage = hishel.AsyncFileStorage(base_path="./.cache/ufc_events/", ttl=3600 * 24)
            async with hishel.AsyncCacheClient(
                storage=storage,
                verify=False,
            ) as client:
                try:
                    res = await client.get(
                        f"https://d29dxerjsp82wz.cloudfront.net/api/v3/event/live/{page}.json",
                        extensions={"force_cache": True},
                    )
                    if res.status_code != 200:
                        logger.error(f"ERROR at page {page}: HTTP ERROR -- {res.status_code}")
                        return
                except Exception as e:
                    logger.error(f"ERROR at page {page}: hishel cache error ??? {e}")
                    return


            json_data = res.json()
            event_details = json_data["LiveEventDetail"]

            if event_details:
                event_data = {
                    "id": event_details["EventId"],
                    "name": event_details["Name"],
                    "date": event_details["StartTime"],
                    "city": event_details["Location"]["City"],
                    "state": event_details["Location"]["State"],
                    "country": event_details["Location"]["Country"],
                    "venue": event_details["Location"]["Venue"],
                }


                async with pool.acquire() as conn:
                    await conn.execute(
                        """
                        INSERT INTO raw_events (id, name, date, city, state, country, venue, last_updated_at)
                        VALUES ($1, $2, $3, $4, $5, $6, $7, CURRENT_TIMESTAMP)
                        ON CONFLICT (id) DO UPDATE SET
                            id = EXCLUDED.id,
                            name = EXCLUDED.name,
                            date = EXCLUDED.date,
                            city = EXCLUDED.city,
                            state = EXCLUDED.state,
                            country = EXCLUDED.country,
                            venue = EXCLUDED.venue,
                            last_updated_at = CURRENT_TIMESTAMP
                        """,
                        event_data["id"],
                        event_data["name"],
                        event_data["date"],
                        event_data["city"],
                        event_data["state"],
                        event_data["country"],
                        event_data["venue"],
                    )
            else:
                logger.info(f"No data found for page {page}")
                pass

            await asyncio.sleep(delay)

        except Exception as e:
            logger.error(f"Error fetching data for page {page}: {str(e)}")
            raise


def create_event_table():
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
    cursor.close()
    conn.close()

async def main():
    create_event_table()

    pool = await asyncpg.create_pool(
        os.getenv("DB_URI"),
        min_size=1,
        max_size=32
    )

    semaphore = asyncio.Semaphore(32)
    tasks = [get_event_data(i, semaphore, pool, 1) for i in range(1, 1300)] 
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
