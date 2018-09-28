from pathlib import Path
import json
import requests
from hashlib import sha256
import gzip
from bs4 import BeautifulSoup as BS
import os
def rdsig(arg):
  link, link_hash = arg
  if os.path.exists(f'darturl_clean/{link_hash}'):
    return
  r = requests.get(link)
  r.encoding = r.apparent_encoding 
  html = r.text
  simple_url = r.url
  simple_hash = sha256(bytes(simple_url, 'utf8')).hexdigest()
  open(f'darturl_clean/{link_hash}', 'w').write( simple_url )
  open(f'htmls/{simple_hash}.gz', 'wb').write( gzip.compress( bytes(html,'utf8') ) ) 

def pickup(arg):
  link, link_hash = arg
  if os.path.exists(f'darturl_clean/{link_hash}'):
    return
  r = requests.get(link)
  r.encoding = r.apparent_encoding 
  html = r.text
  soup = BS(html)
  simple_url = soup.find('a', {'class':'newsLink'}).get('href')
  simple_hash = sha256(bytes(simple_url, 'utf8')).hexdigest()

  r = requests.get(simple_url)
  r.encoding = r.apparent_encoding 
  html = r.text
  open(f'darturl_clean/{link_hash}', 'w').write( simple_url )
  open(f'htmls/{simple_hash}.gz', 'wb').write( gzip.compress( bytes(html,'utf8') ) ) 

  print(simple_url)

from concurrent.futures import ProcessPoolExecutor as PPE

paths = [path for path in Path('./xml_parse').glob('*')]

def pmap(path):
  #print(path)
  obj = json.load(path.open())
  #print( obj )
  link = obj['link']
  link_hash = obj['link_hash']
  
  if 'rdsig.yahoo.co.jp' in link:
    # rdsigは量が多すぎて評価できないので無視する
    print(link)
    rdsig((link, link_hash))
    ...
  else:
    print(link)
    pickup((link, link_hash))

with PPE(max_workers=24) as exe:
  exe.map(pmap, paths)
