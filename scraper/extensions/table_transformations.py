from psycopg2.extensions import quote_ident
from typing import List
import pandas as pd
import psycopg2
import os

def get_column(column_name: str, table_name: str):
  try:
    conn = psycopg2.connect(os.getenv("DB_URI"))
    cursor = conn.cursor()
  except psycopg2.Error as e:
    print(f"Error connecting to PostgresSQL: {e}")
  
  q_col = quote_ident(column_name, cursor)
  q_table = quote_ident(table_name, cursor)
  
  try:
    cursor.execute(f"SELECT {q_col} FROM {q_table}")
    values = cursor.fetchall()
    return [v[0] for v in values]

  except psycopg2.Error as e:
    print(f"Error executing query: {e}")
  
  finally:
    if (conn):
      cursor.close()
      conn.close()
      print("DB connection has been closed")

"""
TODO
 - [x] Get data from SQL table events
 - [x] Get data from json file countries 
 - [ ] Check if there is a match 
 - [ ] If so add the new value cca2 into the table
 Note:
  - If there isnt a match just copy over the country name to cca2
"""
def add_CCA2_to_events(values: List[str]):
  countries_df = pd.read_json('./other_data/countries.json')
  countries = countries_df['name']




print(get_column("country", "events"))
