import os

import glob

import gzip

import bs4, lxml

import concurrent.futures

import re

import hashlib
def _map(arg):
  index, name = arg
  html = gzip.decompress(open(name, 'rb').read()).decode()
  soup = bs4.BeautifulSoup(html, 'lxml')

  for script in soup(["script", "style"]):
    script.extract()    # rip it out

  dds = soup.find_all('div')
  for dd in dds:
    print(dd)

args = [(index,name) for index,name in enumerate(glob.glob('htmls/*'))]
with concurrent.futures.ProcessPoolExecutor(max_workers=1) as exe:
  exe.map( _map, args)
