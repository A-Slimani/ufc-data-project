from datetime import datetime
import psycopg2
import logging
import asyncio
import asyncpg
import hishel
import httpx
import os

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("ufc_events.log"), logging.StreamHandler()],
)

logger = logging.getLogger(__name__)

async def init_db():
    pool = await asyncpg.create_pool(os.getenv("DB_URI"), min_size=1, max_size=20)

    async with pool.acquire() as conn:
        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS events (
                id SERIAL PRIMARY KEY,
                name TEXT,
                date DATE,
                city TEXT,
                state TEXT,
                country TEXT,
                venue TEXT,
                last_updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
            )
            """
        )
    
    return pool

async def get_event_data(client, pool, page):
    try:
        async with hishel.AsyncCacheClient() as client:
            res = await client.get(
                f"https://d29dxerjsp82wz.cloudfront.net/api/v3/event/live/{page}.json"
            )

        json_data = res.json()
        if "LiveEventDetail" in json_data:
            event_details = json_data["LiveEventDetail"]

            date = event_details["StartTime"]
            if date is not None:
                date = datetime.fromisoformat(event_details["StartTime"])

            event_data = {
                "id": event_details["EventId"],
                "name": event_details["Name"],
                "date": date,
                "city": event_details["Location"]["City"],
                "state": event_details["Location"]["State"],
                "country": event_details["Location"]["Country"],
                "venue": event_details["Location"]["Venue"],
            }

            async with pool.acquire() as conn:
                await conn.execute(
                    """
                    INSERT INTO events (id, name, date, city, state, country, venue, last_updated_at)
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
    try:
        pool = await init_db()
        async with httpx.AsyncClient() as client:
            tasks = [get_event_data(client, pool, i) for i in range(1, 1300)]
            await asyncio.gather(*tasks)
    except Exception as e:
        logger.error(f"Error in main: {str(e)}")
        raise
    finally:
        await pool.close()

if __name__ == "__main__":
    asyncio.run(main())
