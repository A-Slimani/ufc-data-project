from collections import defaultdict
from rapidfuzz import fuzz
import xml.etree.ElementTree as ET
import json


NAMESPACE = "{http://www.sitemaps.org/schemas/sitemap/0.9}"

with open("missing_reach.json", "r") as file:
  json_data = json.load(file)

results = defaultdict(dict) 

for i in range(1, 115):
  print('parsing file number: ', i)
  tree = ET.parse(f"./tapology_xmls/tapology_fighters_{i}.xml")
  root = tree.getroot()

  for fighter in json_data:
    f_name = ""
    f_nickname = ""
    first_name = '-'.join(fighter['first_name'].split(' '))
    last_name = '-'.join(fighter['last_name'].split(' '))
    if fighter['nick_name'] is not None:
      nick_name = '-'.join(fighter['nick_name'].split(' '))
      f_nickname = f"{first_name}-{last_name}-{nick_name}".lower()
      f_name = f"{first_name}-{last_name}".lower()
    else:
      f_name = f"{first_name}-{last_name}".lower()

    for e in root.findall(f'{NAMESPACE}url/{NAMESPACE}loc'):
      xml_name_preprocessed = e.text.strip().split('/')[-1].split('-')
      xml_name = ""
      similarity = 0

      if len(xml_name_preprocessed) > 2:
        xml_name = '-'.join(xml_name_preprocessed)
        xml_nickname = '-'.join(xml_name_preprocessed[1:])
        xml_no_nickname = '-'.join(xml_name_preprocessed[:-1])

        s_nickname = fuzz.ratio(xml_nickname, f_nickname) / 100.0
        s_name = fuzz.ratio(xml_name, f_nickname) / 100.0
        s_no_nickname = fuzz.ratio(xml_no_nickname, f_nickname) / 100.0

        s2_nickname = fuzz.ratio(xml_nickname, f_name) / 100.0
        s2_name = fuzz.ratio(xml_name, f_name) / 100.0
        s2_no_nickname = fuzz.ratio(xml_no_nickname, f_name) / 100.0

        options = [
          (xml_nickname, s_nickname),
          (xml_name, s_name),
          (xml_no_nickname, s_no_nickname),
          (xml_nickname, s2_nickname),
          (xml_name, s2_name),
          (xml_no_nickname, s2_no_nickname)
        ]

        xml_name, similarity = max(options, key=lambda x: x[1])

      else:
        xml_name = '-'.join(xml_name_preprocessed)
        similarity = fuzz.ratio(xml_name, f_name) / 100.0

      match = {
        'generated-name': f_name,
        'matched_name': xml_name,
        'similarity': similarity,
        'url': e.text.strip()
      }

      if similarity == 1:
        results[f_name] = match

      # if results[f_name]:
      #   if similarity > results[f_name]['similarity']:
      #     results[f_name] = match
      # else:
      #   if similarity >= 0.8:
      #     results[f_name] = match


# for result, value in results.items():
#   if value['similarity'] > 0.8:
#     count += 1

# print(f">80 matches / total: {count} / {len(json_data)}")

with open('matches.json', 'w') as file:
  json.dump(results, file, indent=2)


