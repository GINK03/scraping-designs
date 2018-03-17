import glob

import json

import pickle

import gzip

import os

import hashlib

import re

import bs4, lxml

import concurrent.futures
URL = 'http://mangamura.org'
def _map(arg):
  key, names = arg
  size = len(names)
  urls = set()
  for index, name in enumerate(names):
    html = gzip.decompress(open('htmls/' + name, 'rb').read()).decode()
    soup = bs4.BeautifulSoup(html, 'lxml')
    for a in soup.findAll('a', href=True):
      url = a.get('href')
      if len(url) >= 2 and url[0] == '/':
        url = URL + url
      if URL not in url:
        continue
      if re.search(r'kai_pc_viewer\?p=', url) is None:
        continue
      print(f'{key} {index}/{size} {url}')
      urls.add(url)
  return urls

args = {}
for index, name in enumerate([name.split('/').pop() for name in glob.glob('htmls/*')]):
  key = index%12
  if args.get(key) is None:
    args[key] = []
  args[key].append( name )
args = [(key,names) for key, names in args.items()]
urls = set()
with  concurrent.futures.ProcessPoolExecutor(max_workers=12) as exe:
  for _urls in exe.map(_map,args) :
    [urls.add(url) for url in _urls]
open('pc_viewer_urls.pkl.gz', 'wb').write(gzip.compress(pickle.dumps(urls)))
