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
URL = 'https://mental.blogmura.com'
def html(url): 
  try:
    url = url.replace('//ameblo.jp//ameblo.jp', '//ameblo.jp')
    print(url)
    save_name = 'htmls/' + hashlib.sha256(bytes(url,'utf8')).hexdigest()
    save_href = 'hrefs/' + hashlib.sha256(bytes(url,'utf8')).hexdigest()
    if os.path.exists(save_name) is True:
      return []
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'}
    try:
      r = requests.get(url, headers=headers)
    except Exception as e:
      print(e)
      return []
    r.encoding = 'EUC-JP'#r.apparent_encoding
    html = r.text
    #print(html)
    try:
      open(save_name, 'wb').write( gzip.compress(bytes(html,'utf8')) )
    except OSError as e:
      print(e)
      return []
    soup = bs4.BeautifulSoup(html, 'lxml')
    #print(soup) 
    hrefs = []
    for href in soup.find_all('a', href=True): 
      _url = href['href']
      #print('in', _url, _url[0:2])
      if len(_url) > 2 and '//' == _url[0:2]:
        _url = 'https:' + _url
      elif len(_url) > 1 and '/' == _url[0:1]:
        _url = URL + _url

      #print('in2', _url)
      if re.search(r'^' + URL, _url) is None: 
        continue
      _url = re.sub(r'\?.*?$', '', _url)
      _url = _url.replace('//ameblo.jp//ameblo.jp', '//ameblo.jp')
      hrefs.append(_url)
      print(_url)
    open(save_href, 'w').write( json.dumps(hrefs) )
    return [href for href in hrefs if os.path.exists('htmls/' + hashlib.sha256(bytes(href,'utf8')).hexdigest()) == False] 
  except Exception as ex:
    print(ex)

def main():
  seed = URL
  urls = html(seed) 
 
  try:
    print('try to load pickled urls')
    urls = pickle.loads( gzip.decompress( open('urls.pkl.gz', 'rb').read() ) )
    print(urls)
    print('finished to load pickled urls')
  except FileNotFoundError as e:
    ...
  while urls != set():
    nextUrls = set()
    with concurrent.futures.ProcessPoolExecutor(max_workers=16) as executor:
      for rurls in executor.map(html, urls):
        for url in rurls:
          nextUrls.add(url)
    urls = nextUrls
    open('urls.pkl.gz', 'wb').write( gzip.compress(pickle.dumps(urls)) )
       
main()
