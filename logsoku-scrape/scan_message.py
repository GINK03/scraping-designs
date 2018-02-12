import glob

import bs4

import concurrent.futures

import os

import re

import json

import hashlib

import gzip

import pickle

import random
def _name(arr):
  index, names = arr

  for name in names:
    try:
      soup = bs4.BeautifulSoup( gzip.decompress(open(name, 'rb').read()) )
      base = soup.find('base')
      if base is None:
        continue

      href = base.get('href')
      messages = [m.text for m in soup.find_all('div', {'class':'message'})]
      for msg in messages: 
        obj = {}
        obj['href'] = href
        obj['msg']  = msg
        if random.random() < 0.01: 
          print(obj)
        data = pickle.dumps(obj)
        ha = hashlib.sha256(bytes(msg, 'utf8')).hexdigest()
        if os.path.exists(f'messages/{ha}'):
          continue
        open(f'messages/{ha}', 'wb').write( data )

    except Exception as ex:
      print(ex)
arr = {}
for index, name in enumerate(glob.glob('htmls/*')):
  key = index%32
  if arr.get(key) is None:
    arr[key] = []
  arr[key].append(name)
arr = [(index,names) for index,names in arr.items()]
#_name(arr[0])
with concurrent.futures.ProcessPoolExecutor(max_workers=32) as exe:
  exe.map(_name, arr)
