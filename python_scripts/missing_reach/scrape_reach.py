from bs4 import BeautifulSoup
import requests
import json

# open json file
with open("matches.json", "r") as file:
    matches = json.load(file)

# go through all the urls 
# for key, value in matches.items(): 
#     print("parsing: ", value['url'])


url = matches['jay-cucciniello']['url']
response = requests.get(url)

soup = BeautifulSoup(response.text, "lxml")

print(soup)
# add to db


