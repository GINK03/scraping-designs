import os
import math
import sys
import urllib.request, urllib.error, urllib.parse
import requests
import http.client
import ssl
import re
import multiprocessing as mp
from socket import error as SocketError
import bs4, lxml
import concurrent.futures
import glob
import pickle
import os
import gzip
import random
import json
import re
import hashlib
import time

try:
  os.mkdir('htmls')
  os.mkdir('hrefs')
except:
  ...
URL = 'http://kakaku.com'
def html(url): 
  try:
    print(url)
    save_name = 'htmls/' + hashlib.sha256(bytes(url,'utf8')).hexdigest()
    save_href = 'hrefs/' + hashlib.sha256(bytes(url,'utf8')).hexdigest()
    if os.path.exists(save_name) is True:
      return []
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:58.0) Gecko/20100101 Firefox/58.0'}
    headers['referer'] = 'https://www.amazon.co.jp'
    try:
      r = requests.get(url, headers=headers)
      #print(r.status_code)
    except Exception as e:
      return []
    #time.sleep(random.randint(3,7))
    r.encoding = r.apparent_encoding
    html = r.text
    # print(html)
    try:
      open(save_name, 'wb').write( gzip.compress(bytes(html,'utf8')) )
    except OSError:
      return []
    soup = bs4.BeautifulSoup(html, 'lxml')
   
    hrefs = []
    for href in soup.find_all('a', href=True): 
      _url = href['href']
      try:
        if '/' == _url[0]:
          _url = URL + _url
      except IndexError as e:
        continue
      if re.search(r'^' + URL, _url) is None: 
        continue
      _url = re.sub(r'\?.*?$', '', _url)
      _url = '/'.join(filter(lambda x:'='not in x, _url.split('/')))
      hrefs.append(_url)
    open(save_href, 'w').write( json.dumps(hrefs) )
    return [href for href in hrefs if os.path.exists('htmls/' + hashlib.sha256(bytes(href,'utf8')).hexdigest()) == False] 
  except Exception as ex:
    print(ex)
    return []

def main():
  seed = 'http://kakaku.com/item/K0000995492/'
  urls = html(seed) 

  if '--resume' in sys.argv:
    try:
      print('try to load pickled urls')
      urls = pickle.loads( gzip.decompress( open('urls.pkl.gz', 'rb').read() ) )
      print('finished to load pickled urls')
    except FileNotFoundError as e:
      ...
  
  while urls != set():
    nextUrls = set()
    with concurrent.futures.ProcessPoolExecutor(max_workers=64) as executor:
      for rurls in executor.map(html, urls):
        for url in rurls:
          nextUrls.add(url)
    urls = nextUrls
    open('urls.pkl.gz', 'wb').write( gzip.compress(pickle.dumps(urls)) )
       
main()
