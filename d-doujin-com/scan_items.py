import os

import glob

import gzip
import requests
import bs4, lxml
import os
import concurrent.futures
import json
import re
import random
import hashlib

URL = 'http://d-doujin.com/'

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

    title = soup.title.text
    print(title)
    h1 = soup.find('h1')
    print(h1.text)

    target_folder = h1.text

    try: 
      os.mkdir(target_folder)
    except: ...

    canonical = soup.find('link', {'href':True, 'rel':'canonical'}).get('href')

    hash256 = hashlib.sha256(bytes(canonical, 'utf8')).hexdigest()
    print(canonical, hash256)

    tables = soup.find('table', {'class':'tag'})
    tags = tables.find_all('a')
    print(tags)

    for img in soup.find_all('img',{'src':True}):
      alt = img.get('alt')
      if not re.search(r'\d{1,}$', alt):
        continue

      print( re.search(r'\d{1,}$', alt).group(0), alt)

      num_img = int( re.search(r'\d{1,}$', alt).group(0) )
      src = img.get('src')
      full_src = URL + src
      print( full_src )
      ri = requests.get( full_src )
      if ri.status_code != 200:
        continue
      with open(f'{target_folder}/{num_img:04d}.jpg', 'wb') as fp: fp.write( ri.content )

      #print(img)
    #json.dump(obj, fp=open(f'parsed/{hash}', 'w'), indent=2, ensure_ascii=False)
    return None
  except Exception as exe:
    print(exe)
    return None

args = [(index,name) for index,name in enumerate(glob.glob('htmls/*'))]

[ _map(arg) for arg in args ]
with concurrent.futures.ProcessPoolExecutor(max_workers=64) as exe:
  exe.map( _map, args)
