import requests

import dbm

import time

import concurrent.futures

import random

import hashlib

import os

try:
  os.mkdir('htmls')
except:
  ...

base_url = 'https://camp-fire.jp/projects/view/{}'

headers = {'User-agent':"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36"}

def _map(arr):
  index, iss = arr
  for i in iss:
    url = base_url.format(i)
    print(f'now scan {url}')
    name = hashlib.sha256(bytes(url,'utf8')).hexdigest()
    if os.path.exists(f'htmls/{name}'):
      continue
    r = requests.get(base_url.format(i), headers = headers)
    #r.encoding = r.apparent_encoding 
    if random.random() < 0.05:
      ##print(r.text)
      ...
    open(f'htmls/{name}', 'w').write( r.text )

arrs = {}
for index, i in enumerate(sorted(range(1, 42333), key=lambda x:x*-1)):
  key = index%32
  if arrs.get(key) is None:
    arrs[key] = []
  arrs[key].append( i )
arrs = [ (index, random.sample(iss, len(iss))) for index, iss in arrs.items() ] 
print("start to scan")
#_map(arrs[-1])
with concurrent.futures.ProcessPoolExecutor(max_workers=32) as ex:
  ex.map(_map, arrs) 
