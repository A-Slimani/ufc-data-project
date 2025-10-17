from multiprocessing import Pool, cpu_count
from collections import defaultdict
from typing import Any

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

  fighter_dict = defaultdict(list) 
  
  # matches = []
  for fighter in json_data:
    f_name = ""
    if fighter['nick_name'] is not None:
      nick_name = '-'.join(fighter['nick_name'].split(' '))
      f_name = f"{fighter['first_name']}-{fighter['last_name']}-{nick_name}".lower()
    else:
      f_name = f"{fighter['first_name']}-{fighter['last_name']}".lower()
  
  
    for e in root.findall(f'{NAMESPACE}url/{NAMESPACE}loc'):
      x_pre = e.text.strip().split('/')[-1].split('-')
      x_name = ''
      similarity = 0

      # nickname or number
      if len(x_pre) > 2:
        x_name_nickname = '-'.join(x_pre[1:])
        x_name = '-'.join(x_pre)

        s_nickname = fuzz.ratio(x_name_nickname, f_name) / 100.0
        s_wo = fuzz.ratio(x_name, f_name) / 100.0

        if s_nickname > s_wo:
          similarity = s_nickname 
          x_name = x_name_nickname
        else:
          similarity = s_wo
          x_name = x_name

      # no nickname and number
      else:
        x_name = '-'.join(x_pre)
        similarity = fuzz.ratio(x_name, f_name) / 100.0
  
      if similarity >= 0.5:
        fighter_dict[f_name].append(
          {
            'generated-name': f_name, 
            'matched_name': x_name, 
            'similarity': similarity, 
            'url': e.text.strip()
          }
        )

  end = time.time()

  return fighter_dict 

if __name__ == "__main__":
  start = time.time()

  # fighter_dict = {}

  with open("missing_reach.json", "r") as file:
    json_data = json.load(file)

  # pre_load_names()

  with Pool(processes=cpu_count()) as pool:
    results = pool.map(process_file, range(1, 115))

  print(results)
  final_result = defaultdict(list)
  for d in results:
     for key, value in d.items():
         final_result[key].extend(value)

  merged_dict = dict(final_result)

  with open('matches.json', 'w') as file:
    json.dump(merged_dict, file, indent=2)

  print(f"matches / missing: {len(merged_dict)} / {len(json_data)}")

  end = time.time()
  print(f"total runtime: {end - start}")

