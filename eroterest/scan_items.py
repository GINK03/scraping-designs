import os

import glob

import gzip

import bs4, lxml
import os
import concurrent.futures
import json
import re
import random
import hashlib
def _map(arg):
  index, name = arg
  try:
    hash = name.split('/').pop()
    if os.path.exists(f'parsed/{hash}'):
      return None
    html = gzip.decompress(open(name, 'rb').read()).decode()
    soup = bs4.BeautifulSoup(html, 'lxml')

    for script in soup(["script", "style"]):
      script.extract()    # rip it out

      h3 = soup.find('h3')
      img = soup.find('div', {'class':'itemImage'}).find('img').get('src')
      clk = soup.find('div', {'class':'clickCnt'}).text
      blg = soup.find('div', {'class':'gotoBlog'}).find('a').get('href')
    if random.random() < 0.1: 
      ...
    obj = [h3.text, hash, img, clk, blg]
    print(obj)

    json.dump(obj, fp=open(f'parsed/{hash}', 'w'), indent=2, ensure_ascii=False)
    return None
  except Exception as exe:
    print(exe)
    return None

args = [(index,name) for index,name in enumerate(glob.glob('htmls/*'))]
_map(args[0])
with concurrent.futures.ProcessPoolExecutor(max_workers=64) as exe:
  exe.map( _map, args)
