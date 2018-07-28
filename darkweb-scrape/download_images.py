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
import re
import hashlib
import time


'''
      session = requests.session()
      session.proxies = {'http':  'socks5h://localhost:9050',
                         'https': 'socks5h://localhost:9050'}
      r = session.get(url, headers=headers)
'''

img_urls = json.load(open('img_urls.json'))

def pmap(img_url):
  #print(img_url) 
  try:
    hashs = hashlib.sha256(bytes(img_url, 'utf8')).hexdigest() 
    type = None
    if re.search(r'.jpg$', img_url) or re.search(r'.jpeg$', img_url):
      type = 'jpg'
    elif re.search(r'.png$', img_url):
      type = 'png'
    else:
      return
    print( os.path.exists(f'images/{hashs}.{type}') )
    if os.path.exists(f'images/{hashs}.{type}'):
      return

    session = requests.session()
    session.proxies = {'http':  'socks5h://localhost:9050',
                       'https': 'socks5h://localhost:9050'}
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'}
    try:
      r = session.get(img_url, headers=headers )
    except Exception as ex:
      print(ex)
      return

    bins = r.content
    with open(f'images/{hashs}.{type}', 'wb') as fp: fp.write(bins)
    print('finish', img_url)
  except Exception as ex:
    print(ex)

from concurrent.futures import ProcessPoolExecutor as PPE
PPE(max_workers=300).map(pmap, img_urls)
