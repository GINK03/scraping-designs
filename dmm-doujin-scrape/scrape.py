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
import chromium
try:
  os.mkdir('htmls')
  os.mkdir('hrefs')
except:
  ...

URL = 'https://www.dmm.com'
def html(url): 
  try:
    print(url)
    save_name = 'htmls/' + hashlib.sha256(bytes(url,'utf8')).hexdigest()
    save_href = 'hrefs/' + hashlib.sha256(bytes(url,'utf8')).hexdigest()
    if os.path.exists(save_name) is True:
      return []
    
    html = chromium.getHTML(url) 
    open(save_name, 'wb').write( gzip.compress(bytes(html,'utf8')) )

    soup = bs4.BeautifulSoup(html, 'lxml')
   
    hrefs = []
    for href in soup.find_all('a', href=True): 
      sub_url = href['href']
      if sub_url[0] == '/' and sub_url[1] != '/':
        sub_url = URL + sub_url
      if '/doujin/' not in sub_url:
        continue
      sub_url = re.sub(r'\?.*?$', '', sub_url)
      print(sub_url, re.sub(r'\?.*?$', '', sub_url) )
      hrefs.append(sub_url)
    open(save_href, 'w').write( json.dumps(hrefs) )
    return [href for href in hrefs if os.path.exists('htmls/' + hashlib.sha256(bytes(href,'utf8')).hexdigest()) == False] 
  except Exception as ex:
    print(ex)
    return []

import click
@click.command()
@click.option('--resume', default=True, help='recover from pickle')
def main(resume):
  seed = 'https://www.dmm.co.jp/dc/doujin/-/detail/=/cid=d_134159/'
  urls = html(seed) 
  print(urls)
  if resume is True:
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
    print(urls)
    open('urls.pkl.gz', 'wb').write( gzip.compress(pickle.dumps(urls)) )

if __name__ == '__main__':
  main()
