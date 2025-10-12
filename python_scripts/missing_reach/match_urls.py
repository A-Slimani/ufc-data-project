import xml.etree.ElementTree as ET
from difflib import SequenceMatcher, get_close_matches
import threading
import asyncio
import json
import time

start = time.time()

def similarity_ratio(s1, s2):
  return SequenceMatcher(None, s1, s2).ratio()

json_data = []
with open("missing_nulls.json", "r") as file:
  json_data = json.load(file)

# for fighter in json_data:
#   print(f"{fighter['first_name']}-{fighter['last_name']}")

NAMESPACE = "{http://www.sitemaps.org/schemas/sitemap/0.9}"

def process_file(i):
  tree = ET.parse(f"./tapology_xmls/tapology_fighters_{i}.xml")
  root = tree.getroot()

  def match_fighter(fighter, root):
    name = f"{fighter['first_name']}-{fighter['last_name']}".lower() 
    # print(f"searching for: {name}")
    for e in root.findall(f'{NAMESPACE}url/{NAMESPACE}loc'):
      name2 = "-".join(e.text.strip().split('/')[-1].split('-')[1:])
      s = similarity_ratio(name, name2)
      if s >= 0.95:
        print(name, name2, s)

  threads = []
  for fighter in json_data:
    t = threading.Thread(target=match_fighter, args=(fighter, root))
    t.start()
    threads.append(t)
  
  for t in threads:
    t.join()




# STANDARD
# for i in range(1, 115):
#  process_file(i)

# MULTITHREADED
threads = []
for i in range(1, 115):
  t = threading.Thread(target=process_file, args=(i,))
  t.start()
  threads.append(t)

for t in threads:
  t.join()

# ASYNCHRONOUS
# async def main():
#   coroutines = [process_file(i) for i in range(1, 115)]
#   await asyncio.gather(*coroutines)
#   
# asyncio.run(main())

  
end = time.time()

print(f"Execution time: {end - start} seconds")