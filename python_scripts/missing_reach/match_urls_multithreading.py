from rapidfuzz import fuzz
from multiprocessing import Pool, cpu_count
import xml.etree.ElementTree as ET
import threading
import asyncio
import json
import time

NAMESPACE = "{http://www.sitemaps.org/schemas/sitemap/0.9}"

json_data = []
with open("missing_reach.json", "r") as file:
  json_data = json.load(file)


def process_file(i):
  print(f"Starting process {i}")
  start = time.time()
  tree = ET.parse(f"./tapology_xmls/tapology_fighters_{i}.xml")
  root = tree.getroot()

  all_fighters = []
  for fighter in json_data:
    f_name = "" 
    if fighter['nick_name'] == None:
      f_name = f"{fighter['first_name']}-{fighter['last_name']}".lower()
    else:
      nick_name = '-'.join(fighter['nick_name'].split(' '))
      f_name = f"{fighter['first_name']}-{fighter['last_name']}-{nick_name}".lower()

    current_fighter = {'full_name': f_name, 'matches': []}

    current_matches = []

    for e in root.findall(f'{NAMESPACE}url/{NAMESPACE}loc'):
      x_name = '-'.join(e.text.strip().split('/')[-1].split('-')[1:])
      similarity = fuzz.ratio(x_name, f_name) / 100.0 
      if similarity >= 0.8:
        current_matches.append((fighter, e.text.strip(), similarity))

    current_fighter['matches'] = current_matches
    all_fighters.append(current_fighter)

  end = time.time()
  # print(matches) 
  print(f"File id:{i} process complete. Execution time: {end - start} seconds")

  return all_fighters


if __name__ == "__main__":
  with Pool(processes=cpu_count()) as pool:
    results = pool.map(process_file, range(1, 115))

  complete_results = [r for sublist in results for r in sublist]

  count = 0
  for r in complete_results:
    if r['matches'] != []:
      count += 1

  print(f"url match percentage: {count / len(complete_results)}")

  with open('matches.json', 'w') as file:
    json.dump(complete_results, file, indent=2)

