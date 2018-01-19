import os

import glob

import gzip

import bs4, lxml

import concurrent.futures

import re

import hashlib
def _map(arg):
  name = arg
  html = gzip.decompress(open(name, 'rb').read())
  soup = bs4.BeautifulSoup(html, 'lxml')

  for script in soup(["script", "style"]):
    script.extract()    # rip it out

  center = soup.find('div', {'id':'centerCol'})
  if center is None:
    return
  print( name )
  text = re.sub(r'\s{1,}', ' ', center.text.strip())

  sha = hashlib.sha256( bytes(text, 'utf8') ).hexdigest()

  open('items/{}'.format(sha), 'w').write( text )

names = [name for name in glob.glob('htmls/*')]
with concurrent.futures.ProcessPoolExecutor(max_workers=64) as exe:
  exe.map( _map, names)
