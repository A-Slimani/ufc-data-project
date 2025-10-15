import xml.etree.ElementTree as ET

NAMESPACE = "{http://www.sitemaps.org/schamas/sitemaps/0.9"

for i in range(1, 115):
  root = ET.parse(f"./tapology_xmls/tapology_fighters_{i}.xml").getroot()

  for e in root.finall(f"{NAMESPACE}url/{NAMESPACE}loc"):
    name = '-'.join(e.text.strip().split('/')[-1].split('-')[1:])


