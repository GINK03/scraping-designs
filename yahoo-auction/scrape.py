import requests
from bs4 import BeautifulSoup as BS
import hashlib 
import os
import gzip
import pickle
import sys
import re
import random
url = 'https://auctions.yahoo.co.jp/category/list/S%E3%82%B5%E3%82%A4%E3%82%BA-%E9%95%B7%E8%A2%96T%E3%82%B7%E3%83%A3%E3%83%84-%E3%83%88%E3%83%83%E3%83%97%E3%82%B9-%E5%A5%B3%E6%80%A7%E7%94%A8-%E3%82%B9%E3%83%9D%E3%83%BC%E3%83%84%E3%82%A6%E3%82%A8%E3%82%A2-%E3%82%B9%E3%83%9D%E3%83%BC%E3%83%84-%E3%83%AC%E3%82%B8%E3%83%A3%E3%83%BC/2084263740/?p=S%E3%82%B5%E3%82%A4%E3%82%BA&auccat=2084263740&aucminprice=5000&aucmaxprice=5999&exflg=1&b=1&n=20&s1=featured&slider=undefined'

user_agent = {"Accept-Language": "ja-JP,ja;q=0.5", 'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}
#proxys = [ {'http':f'http://{es[0]}:{es[1]}'} for es in [ line.strip().split() for line in open('proxys') ] ]

def pmap(arg):
  key, urls = arg
  hrefs = set()
  for index, url in enumerate(urls):
    if 'category/list' not in url:
      continue 
    try:
      url_hash = hashlib.sha256(bytes(url, 'utf8')).hexdigest()
      if key != -1 and ( os.path.exists(f'htmls/{url_hash}') or os.path.exists(f'htmls_noise/{url_hash}')):
        #print('already', url)
        continue
      print(key, index, len(urls), url)
      try:
        r = requests.get(url, headers=user_agent, timeout=5)
        r.encoding = 'utf8'
        print(r.text)
      except Exception as ex: 
        print(ex)
        continue

      if 'category/list' in url:
        open(f'htmls/{url_hash}','wb').write( gzip.compress(bytes(r.text,'utf8')) )
      else:
        open(f'htmls_noise/{url_hash}','wb').write( gzip.compress(bytes(r.text,'utf8')) )

      soup = BS(r.text, 'html.parser')
      for a in soup.find_all('a', {'href':True}):
        href = a.get('href')
        if 'https://auctions.yahoo.co.jp/' not in href: continue
        #href = re.sub(r'\?.*?$', '', href)
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

DIST = 1
args = { key:[] for key in range(DIST) }
[ args[index%DIST].append(url) for index, url in enumerate(urls) ] 
args = [ (key,urls) for key, urls in args.items() ]
#[ pmap(arg) for arg in args ]

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

