
import glob
import os
import re
import json


year_freq = {}
for fn in glob.glob('./jsons/*.json'):
  obj = json.load(open(fn))
  case_number = obj['事件番号']
  year = re.search(r'((昭和|平成)\d{1,})', case_number).group(1)
  text = obj['text']
  #if '昭和' in year:
  #  print(text)
  if year_freq.get(year) is None:
    year_freq[year] = {'all':0, '強盗':0}
  year_freq[year]['all'] += 1
  if '強盗' in text:
    year_freq[year]['強盗'] += 1

for year, freq in sorted(year_freq.items()):
  print(year, freq['強盗']/freq['all'])
