import requests
import json

url_list = []
results = [] 

with open('urls.txt', 'r') as file:
    for line in file:
        url_list.append(line.strip())

for url in url_list:
    try: 
        response = requests.get(url)
        data = response.json()
        results.append(data)
        print(f"Success: {url}")
    except:
        print(f"Error when scraping url: {url}")

try:
    with open('all_response.json', 'w') as file:
        json.dump(results, file, indent=2)
    print("json dump success")
except Exception as e:
    print(f"json dump failed, {e}")



