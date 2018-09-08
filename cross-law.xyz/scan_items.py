import os

import glob

import gzip

import bs4, lxml
import os
import concurrent.futures
import json
import re
import random
import hashlib
def _map(arg):

  day_freq = {}

  index, name = arg
  try:
    hash = name.split('/').pop()
    if os.path.exists(f'parsed/{hash}'):
      return None
    html = gzip.decompress(open(name, 'rb').read()).decode()
    soup = bs4.BeautifulSoup(html, 'lxml')

    for script in soup(["script", "style"]):
      script.extract()  
    #print( soup.find('h1') )
    try:
      dts = soup.find('dl').find_all('dt')
      dds = soup.find('dl').find_all('dd')
    except:
      return day_freq
    for dd, dt in zip(dds, dts): 
      dttext = (dt.text)
      try:
        m = re.search(r'(\d\d\d\d/\d\d/\d\d)\(.*?\)\s(\d\d:\d\d)', dttext)
        day      = m.group(1)
        hour_min = m.group(2)
      except:
        continue
      #from collections import namedtuple
      #Item = namedtuple('Item', ('title', 'url', 'user', 'body'))
 
      if day_freq.get(day) is None:
        day_freq[day] = { 'write':0, 'sacred':0 }
      day_freq[day]['write'] += 1
      
      if '唐澤貴洋殺す' in dd.text:
        day_freq[day]['sacred'] += 1
        
      #print(dd.text)
    return day_freq
  except Exception as exe:
    print(exe)
    return None

args = [(index,name) for index,name in enumerate(glob.glob('htmls/*'))]
#day_freq = _map(args[0])

day_freq = {}
with concurrent.futures.ProcessPoolExecutor(max_workers=64) as exe:
  for _day_freq in exe.map( _map, args):
    for day, freq in _day_freq.items():
      if day_freq.get(day) is None:
        day_freq[day] = { 'write':0, 'sacred':0 } 
      day_freq[day]['write'] += freq['write']
      day_freq[day]['sacred'] += freq['sacred']

for day, freq in sorted(day_freq.items()):
  print(day, freq['write'], freq['sacred'])
