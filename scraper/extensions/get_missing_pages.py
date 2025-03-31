from typing import List

def get_missing_page_list(dir) -> List[int]:
  numbers = []
  with open(dir) as file:
    for line in file:
      number = int(line.strip())
      numbers.append(number)
  return numbers


            