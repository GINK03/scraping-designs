
from pathlib import Path

import pickle

import gzip

import bs4, lxml

import re

from urllib.parse import *

import concurrent.futures

import hashlib

import json

import random
def _map(arg):
  key, names = arg
  for name in names:
    try:
      html = gzip.decompress(name.open('rb').read()).decode()

      soup = bs4.BeautifulSoup(html, 'lxml')
      
      keywords = soup.find('meta', {'name':'keywords'})
      if keywords is None:
        continue
      keywords = keywords.get('content')
      canonical = soup.find('link', rel='canonical')
      if canonical is None:
        continue
      canonical = canonical.get('href')
      if 'http://kakaku.com/item/' not in canonical:
        continue
      if 'spec' in canonical or 'picture' in canonical:
        continue

      mainLeft = soup.find('div', {'id':'mainLeft'})
      if mainLeft is None:
        continue
      table = mainLeft.find('table')
      if table is None:
        continue
      #print( re.sub(r'\s{1,}', ' ',table.text) )
      #shops = [ unquote([x for x in href.get('href').split('&') if re.search(r'Url=', x) ].pop()) \
      #    for href in table.findAll('a',href=True) if re.search(r'^http://c.kakaku.com/forwarder/forward.aspx', href.get('href')) ]
      shops = [ href.get('href') \
          for href in soup.findAll('a',href=True) if re.search(r'^http://kakaku.com/ksearch/redirect/', href.get('href')) ]
      if shops != []:
        shops = [ re.search(r'\?=(.*?)', x).group(1) for x in shops if re.search(r'\?=', x) ] 
      if shops == []:
        shops = [ href.get('href') \
          for href in soup.findAll('a',href=True) if re.search(r'^http://c.kakaku.com/forwarder/forward.aspx', href.get('href')) ]
        shops = [ [x for x in href.split('&') if re.search(r'Url=', x)] for href in shops ]
        shops = [ unquote(x.pop()) for x in shops if x != [] ]
      if random.random() < 0.01:
        print( canonical )
        print( keywords )
        print( shops)
      if shops == []:
        continue
      obj = {'canonical':canonical, 'keywords':keywords, 'shops':shops}
      ha = hashlib.sha256(bytes(canonical, 'utf8')).hexdigest()
      json.dump( obj, open(f'canonical_shops/{ha}', 'w'), indent=2, ensure_ascii=False)
    except Exception as ex:
      print(ex)

args = {}
for index,name in enumerate(Path('./htmls').glob('*')):
  key = index%16
  if args.get(key) is None:
    args[key] = []
  args[key].append( name )
args = [(key, names) for key, names in args.items() ]

with concurrent.futures.ProcessPoolExecutor(max_workers=16) as exe:
  exe.map(_map, args)
