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

  center = soup.find('div', {'id':'contentMain-inner'})
  if center is None:
    return
  print( index, name )
  text = re.sub(r'\s{1,}', ' ', center.text.strip())

  sha = hashlib.sha256( bytes(text, 'utf8') ).hexdigest()

  open('items/{}'.format(sha), 'w').write( text )

args = [(index,name) for index,name in enumerate(glob.glob('htmls/*'))]
with concurrent.futures.ProcessPoolExecutor(max_workers=64) as exe:
  exe.map( _map, args)
