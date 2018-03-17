import glob

import json

import pickle

import gzip

import os

import hashlib

import re

import bs4, lxml
names = set([name.split('/').pop() for name in glob.glob('htmls/*')])

URL = 'http://mangamura.org'
urls = set()
for name in names:
  html = gzip.decompress(open('htmls/' + name, 'rb').read()).decode()
  soup = bs4.BeautifulSoup(html, 'lxml')
  for a in soup.findAll('a', href=True):
    url = a.get('href')
    if len(url) >= 2 and url[0] == '/':
      url = URL + url
    if URL not in url:
      continue
    print(url)
    urls.add(url)
open('urls.pkl.gz', 'wb').write(gzip.compress(pickle.dumps(urls)))
