import requests
from bs4 import BeautifulSoup as BS
import hashlib 
import os
import gzip
import pickle
import sys
import re
url = 'https://item.mercari.com/jp/m54354648824/'

user_agent = {'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}

def pmap(arg):
  key, urls = arg
  hrefs = set()
  for index, url in enumerate(urls):
    try:
      url_hash = hashlib.sha256(bytes(url, 'utf8')).hexdigest()
      if key != -1 and os.path.exists(f'htmls/{url_hash}'):
        continue
      print(key, url, index, len(urls))
      try:
        r = requests.get(url, headers=user_agent, timeout=1)
      except Exception as ex: 
        print(ex)
        continue
      open(f'htmls/{url_hash}','wb').write( gzip.compress(bytes(r.text,'utf8')) )
      soup = BS(r.text, 'html.parser')
      for a in soup.find_all('a', {'href':True}):
        if 'https://www.mercari.com' not in a.get('href'): continue
        href = a.get('href')
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

