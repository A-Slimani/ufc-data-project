import httpx
import asyncio
from httpx import HTTPStatusError, RequestError

BASE_URL = "https://www.tapology.com/fightcenter/fighters/sitemap"
MAX_RETRIES = 10

async def get_links(index, semaphore, client):
  url = f"{BASE_URL}_{index}.xml" if index > 1 else f"{BASE_URL}_{index}.xml"
  for attempt in range(MAX_RETRIES):
    try:
      async with semaphore:
        print(f'scraping index: {index}, Attempt: { attempt + 1 } / { MAX_RETRIES }')

        response = await client.get(url, timeout=30.0)

        response.raise_for_status()

        with open(f'./tapology_xmls/tapology_fighters_{index}.xml', 'w') as file:
          file.write(response.text)
        
        print(f"scraping {index} success")
        return

    except HTTPStatusError as e:
      if e.response.status_code == 503:
        if attempt < MAX_RETRIES - 1:
          await asyncio.sleep(10)
          continue
        else:
          print(f"failed to scrape {index} after {MAX_RETRIES}")
          break
      else:
        print(f"Non retryable HTTP Error {e.response.status_code} for index {index}")


async def main():
  semaphore = asyncio.Semaphore(32)
  async with httpx.AsyncClient() as client:
    tasks = [get_links(i, semaphore, client) for i in range(1, 115)]

    await asyncio.gather(*tasks)

if __name__ == '__main__':
  asyncio.run(main())
