import requests
from bs4 import BeautifulSoup as BS
import hashlib 
import os
import gzip
import pickle
import sys
import re
import random
url = 'https://item.mercari.com/jp/m54354648824/'

user_agent = {"Accept-Language": "ja-JP,ja;q=0.5", 'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}
proxys = [ {'http':f'http://{es[0]}:{es[1]}'} for es in [ line.strip().split() for line in open('proxys') ] ]

def pmap(arg):
  key, urls = arg
  hrefs = set()
  for index, url in enumerate(urls):
    try:
      url_hash = hashlib.sha256(bytes(url, 'utf8')).hexdigest()
      if key != -1 and os.path.exists(f'htmls/{url_hash}'):
        print('already', url)
        continue
      if '/us/' in url:
        continue
      print(key, url, index, len(urls))
      try:
        r = requests.get(url, headers=user_agent, timeout=1, proxies=random.choice(proxys))
      except Exception as ex: 
        print(ex)
        continue
      open(f'htmls/{url_hash}','wb').write( gzip.compress(bytes(r.text,'utf8')) )
      soup = BS(r.text, 'html.parser')
      for a in soup.find_all('a', {'href':True}):
        href = a.get('href')
        print(href)
        href = re.sub(r'\?.*?$', '', href)
        hrefs.add(a.get('href'))
    except Exception as ex:
      print(ex)
      continue
  return hrefs
  
if '--resume' in sys.argv:
  urls = pickle.load(open('urls.pkl', 'rb') )
else:
  urls = pmap((-1, [url]))
  print(urls)

DIST = 25
args = { key:[] for key in range(DIST) }
[ args[index%DIST].append(url) for index, url in enumerate(urls) ] 
args = [ (key,urls) for key, urls in args.items() ]
#[ pmap(arg) for arg in args]
from concurrent.futures import ProcessPoolExecutor as PPE
while True:
  with PPE(max_workers=DIST) as exe:
    urls = set()
    for _hrefs in exe.map(pmap, args):
      urls |= _hrefs 
  pickle.dump( urls, open('urls.pkl', 'wb') )
  args = { key:[] for key in range(DIST) }
  [ args[index%DIST].append(url) for index, url in enumerate(urls) ] 
  args = [ (key,urls) for key, urls in args.items() ]

