import glob

import json

import pickle

import gzip

import os

import hashlib

import re

import bs4

import concurrent.futures

names = set([name.split('/').pop() for name in glob.glob('hrefs/*')])
size = len(names)

def _map(arg):
  urls = set()
  index, size, name = arg
  print(index, '/', size, name)
  try:
    html = gzip.decompress(open(f'htmls/{name}', 'rb').read()).decode()
  except Exception as ex:
    return []
  soup = bs4.BeautifulSoup(html)
  for a in soup.find_all('a', href=True):
    href = a.get('href')
    href = re.sub(r'\?.*?', '', href)
    href = '/'.join(filter(lambda x:'='not in x, href.split('/')))
    #print(href)
    if 'https://www.dmm.com' in href:
      urls.add(href)
  return urls

urls = set()
args = [(index, size, name) for index, name in enumerate(names)]
_map(args[0])
with concurrent.futures.ProcessPoolExecutor(max_workers=16) as exe:
  for _urls  in exe.map(_map, args):
    for url in _urls:
      urls.add(url)
  
print(urls)
open('urls.pkl.gz', 'wb').write(gzip.compress(pickle.dumps(urls)))
