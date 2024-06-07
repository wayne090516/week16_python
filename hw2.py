import requests
import re
import pandas as pd
from tabulate import tabulate

all_data = []

for i in range(100):
  url = f'https://exam.naer.edu.tw/searchResult.php?page={i}&orderBy=lastest&keyword=&selCountry=&selCategory=0&selTech=0&selYear=&selTerm=&selType=&selPublisher='
  res = requests.get(url)
    
  if res.status_code == 200:
    page_content = res.text

    pattern = re.compile(r'<tr><td.+?>(?P<city>[^<]+)</td><td.+?</td><td.+?>(?P<grade>[^<]+)</td><td.+?</td><td.+?</td><td.+?>(?P<subject>[^<]+)</td>')
    matches = pattern.finditer(page_content)
        
    for match in matches:
      data = match.groupdict()
      all_data.append(data)
  else:
      print(f"Failed to retrieve page {i}.")

df = pd.DataFrame(all_data)
df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

def grade_sort_key(grade):
  order = {
    '一年級': 1, '二年級': 2, '三年級': 3, '四年級': 4, '五年級': 5, '六年級': 6,
    '七年級': 7, '八年級': 8, '九年級': 9, '高一': 10, '高二': 11, '高三': 12
  }
  return order.get(grade, 100)

cities = df['city'].unique()
for city in cities:
  city_data = df[df['city'] == city]
  pivot_table = pd.pivot_table(city_data, index='subject', columns='grade', aggfunc='size', fill_value=0)
  pivot_table.index.name = city
  pivot_table = pivot_table.reindex(sorted(pivot_table.columns, key=grade_sort_key), axis=1)
  print(tabulate(pivot_table, headers='keys', tablefmt='grid'))