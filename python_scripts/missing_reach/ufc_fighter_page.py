import httpx
import json

# list of all the potential fighters to scrape
with open('missing_nulls.json') as file:
    data = json.load(file)

for fighter in data:
    print(f"{fighter['first_name']}-{fighter['last_name']}".lower())
