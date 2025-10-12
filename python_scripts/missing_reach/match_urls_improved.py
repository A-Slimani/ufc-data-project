import xml.etree.ElementTree as ET
from difflib import SequenceMatcher, get_close_matches
import json
import time

start = time.time()

json_data = []
with open("missing_nulls.json", "r") as file:
  json_data = json.load(file)

NAMESPACE = "{http://www.sitemaps.org/schemas/sitemap/0.9}"


def process_file(i):
  tree = ET.parse(f"./tapology_fighter_xmls/tapology_fighters_{i}.xml")
  root = tree.getroot()

  for fighter in json_data:

    for e in root.findall(f'{NAMESPACE}url/{NAMESPACE}loc'):
      f_name = '-'.join(e.text.strip().split('/')[-1].split('-')[1:]) 
      s = SequenceMatcher(None, name, f_name).ratio()
    

    
for i in range(1, 115):
  print(process_file(i))


end = time.time()

print(f"Execution time: {end - start} seconds")
