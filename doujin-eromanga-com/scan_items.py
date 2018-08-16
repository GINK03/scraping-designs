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
    html = gzip.decompress(open(name, 'rb').read()).decode()
    soup = bs4.BeautifulSoup(html, 'lxml')

    for script in soup(["script", "style"]):
      script.extract()    # rip it out
    
    try:
      canonical = soup.find('link', {'href':True, 'rel':'canonical'}).get('href')
    except: return

    title = soup.title.text
    print(title)
    h2 = soup.find('h2')
    print(h2.text)
    
    target_folder = 'folders/' + h2.text
    try: 
      os.mkdir(target_folder)
    except: ...
    

    tags = [a.text for a in soup.find('dl', {'class':'article-tags'}).find_all('a')]
    print(tags)

    article = soup.find('div', {'id':'main-contents'})
    for num_img, img in enumerate(article.find_all('img',{'src':True})):

      src = img.get('src')
      full_src = src
      print( full_src )
      ri = requests.get( full_src )
      if ri.status_code != 200:
        continue
      with open(f'{target_folder}/{num_img:04d}.jpg', 'wb') as fp: fp.write( ri.content )

      #print(img)
    obj = {'url':canonical, 'tags':tags} 
    hash256 = hashlib.sha256(bytes(canonical, 'utf8')).hexdigest()
    print(canonical, hash256)
    json.dump(obj, fp=open(f'{target_folder}/{hash256}.json', 'w'), indent=2, ensure_ascii=False)
    return None
  except Exception as ex:
    print(ex)
args = [(index,name) for index,name in enumerate(glob.glob('htmls/*'))]

#[ _map(arg) for arg in args ]
with concurrent.futures.ProcessPoolExecutor(max_workers=128) as exe:
  exe.map( _map, args)
