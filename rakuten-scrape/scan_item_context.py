import json

import glob

import bs4

import re

import hashlib

import concurrent.futures

import dbm
def _map(arr):
  index, names = arr
  for ind, name in enumerate(names):
    try:
      soup = bs4.BeautifulSoup(open(name).read())
      rel = soup.find('link', {'rel':'canonical'})
      if rel is None: continue
      href = (rel.get('href'))

      sha = hashlib.sha256(bytes(href,'utf8')).hexdigest() 
      if re.search(r'https://item.rakuten.co.jp/', href) is None:
        continue

      item = soup.find('span', {'class':'item_name'})
      if item is None:
        continue
      item = item.text
      desc = soup.find('span', {'class':'item_desc'})
      if desc is None:
        continue
      desc = re.sub(r'\s{1,}', ' ', desc.text.strip())

      print(ind, item, desc)
      open('items/{}'.format(sha), 'w').write( json.dumps({'item':item, 'desc':desc}, indent=2, ensure_ascii=False) )
    except Exception as ex:
      print(ex)

arr = {}
for index, name in enumerate(glob.glob('htmls/*')):
  key = index%32
  if arr.get(key) is None:
    arr[key] = []
  arr[key].append( name )
arr = [ (index, names) for index, names in arr.items() ]

#_map(arr[0])
with concurrent.futures.ProcessPoolExecutor(max_workers=32) as exe:
  exe.map( _map, arr )
