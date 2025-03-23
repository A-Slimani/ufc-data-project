import pandas as pd

def clean_events():
  # Create a new column of full name countries into country codes
  countries = pd.read_json('./other_data/countries.json')
  df = pd.DataFrame(countries) 


clean_events()