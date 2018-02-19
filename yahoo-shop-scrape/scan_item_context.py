import json

import glob

import bs4, lxml

import re

import hashlib

import concurrent.futures

import dbm

import os

import gzip
def _map(arr):
    index, names = arr
    for ind, name in enumerate(names):
      try:
        sha = name.split('/').pop()
        if os.path.exists('items/{}'.format(sha) ) is True:
          continue
        
        soup = bs4.BeautifulSoup( gzip.decompress(open(name, 'rb').read()).decode(), 'lxml')
        #print(name)
        rel = soup.find('link', {'rel':'canonical'})
        #print(rel)
        if rel is None:  
          continue
        href = rel.get('href') if rel else ''
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
arrs = {}
for index, name in enumerate(glob.glob('htmls/*')):
  key = index%32
  if arrs.get(key) is None:
    arrs[key] = []
  arrs[key].append( name )
arrs = [ (index, names) for index, names in arrs.items() ]

#for arr in arrs:
#  _map(arr)
with concurrent.futures.ProcessPoolExecutor(max_workers=16) as exe:
  exe.map( _map, arrs )
