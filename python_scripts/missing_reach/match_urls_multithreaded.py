from multiprocessing import Pool, cpu_count
from collections import defaultdict
from rapidfuzz import fuzz
import xml.etree.ElementTree as ET
import threading
import asyncio
import json
import time

NAMESPACE = "{http://www.sitemaps.org/schemas/sitemap/0.9}"

def pre_load_names(fighter_dict):
  for fighter in json_data:
    f_name = ""
    if fighter['nick_name'] is not None:
      nick_name = '-'.join(fighter['nick_name'].split(' '))
      f_name = f"{fighter['first_name']}-{fighter['last_name']}-{nick_name}".lower()
    else:
      f_name = f"{fighter['first_name']}-{fighter['last_name']}".lower()
    fighter_dict[f_name] = [] 

def process_file(i):
  print(f"Starting process {i}")
  tree = ET.parse(f"./tapology_xmls/tapology_fighters_{i}.xml")
  root = tree.getroot()

  fighter_dict = defaultdict(dict) 
 
  # matches = []
  for fighter in json_data:
    f_name = ""
    if fighter['nick_name'] is not None:
      nick_name = '-'.join(fighter['nick_name'].split(' '))
      f_name = f"{fighter['first_name']}-{fighter['last_name']}-{nick_name}".lower()
    else:
      f_name = f"{fighter['first_name']}-{fighter['last_name']}".lower()
 
 
    for e in root.findall(f'{NAMESPACE}url/{NAMESPACE}loc'):
      xml_name_preprocessed = e.text.strip().split('/')[-1].split('-')
      xml_name = ''
      similarity = 0

      # nickname or number
      if len(xml_name_preprocessed) > 2:
        xml_nickname = '-'.join(xml_name_preprocessed[1:])
        xml_name = '-'.join(xml_name_preprocessed)
        xml_no_nickname = '-'.join(xml_name_preprocessed[:-1])

        s_nickname = fuzz.ratio(xml_nickname, f_name) / 100.0
        s_name = fuzz.ratio(xml_name, f_name) / 100.0
        s_no_nickname = fuzz.ratio(xml_no_nickname, f_name) / 100.0

        options = [
          (xml_nickname, s_nickname),
          (xml_name, s_name),
          (xml_no_nickname, s_no_nickname)
        ]

        xml_name, similarity = max(options, key=lambda x: x[1])

      # no nickname and number 
      else:
        xml_name = '-'.join(xml_name_preprocessed)
        similarity = fuzz.ratio(xml_name, f_name) / 100.0

      match = {
        'generated-name': f_name,
        'matched_name': xml_name,
        'similarity': similarity,
        'url': e.text.strip()
      }
 
      if fighter_dict[f_name]:
        if fighter_dict[f_name]['similarity'] < match['similarity']:
          fighter_dict[f_name] = match
      elif similarity >= 0.8:
        fighter_dict[f_name] = match

  end = time.time()

  return fighter_dict 

if __name__ == "__main__":
  start = time.time()

  # fighter_dict = {}

  with open("missing_reach.json", "r") as file:
    json_data = json.load(file)

  # pre_load_names()

  with Pool(processes=cpu_count()) as pool:
    results = pool.map(process_file, range(1, 5))

  final_results = defaultdict(dict) 

  for result in results:
    for key, value in result.items():
      if final_results[key]:
        # if final_results[key]['similarity'] < result[key]['similarity']:
        #   final_results[key] = result[key]
        # print(final_results[key]['similarity'])
        print(key, final_results[key], result[key]['similarity'])
      else:
          final_results[key] = result[key]

  with open('matches.json', 'w') as file:
    json.dump(results, file, indent=2)


  print(f"matches / total: {len(results)} / {len(json_data)}")

  end = time.time()
  print(f"total runtime: {end - start}")

