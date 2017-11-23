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
import bs4
import concurrent.futures
import pickle
import os
import gzip
import random
import json

proxies = []
for name, ip in json.loads(open('misc/name_ip.json').read() ).items():
  proxies.append( {'http': '{}:8080'.format(ip), 'https':'{}:8080'.format(ip) })
  print(ip)

def html_fetcher(url):
  
  save_name = 'htmls/' + url.replace('/', '_')
  if os.path.exists(save_name) is True:
    return []
  headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'}
  proxy = random.choice(proxies)
  print( proxy )
  r = requests.get(url, proxies=proxy, headers=headers)
  html = r.text
  open(save_name, 'w').write( html )
  soup = bs4.BeautifulSoup(html)
 
  hrefs = []
  for href in soup.find_all('a', href=True): 
    _url = href['href']
    try:
      if '/' == _url[0]:
        _url = 'http://www.itmedia.co.jp' + _url
    except IndexError as e:
      continue
    if 'http://www.itmedia.co.jp' not in _url: continue
    #print(_url)
    hrefs.append(_url)

  print(url)
  return hrefs


def main():
  seed = 'http://www.itmedia.co.jp/'
  urls =  html_fetcher(seed) 
 
  try:
    urls = pickle.loads( gzip.decompress( open('urls.pkl.gz', 'rb').read() ) )
  except FileNotFoundError as e:
    ...
  while True:
    nextUrls = set()
    with concurrent.futures.ThreadPoolExecutor(max_workers=64) as executor:
      for rurls in executor.map(html_fetcher, urls):
        for url in rurls:
          nextUrls.add(url)
    #for urls in [html_fetcher(url) for url in urls]:
    urls = nextUrls
    open('urls.pkl.gz', 'wb').write( gzip.compress(pickle.dumps(urls)) )
       
main()
