import bs4

import MeCab

import dbm

import os

import pickle

import glob

import concurrent.futures

import hashlib

import json
m = MeCab.Tagger("-Owakati")

def _map(name):
  print(name)
  db = dbm.open(name)
  url_vals = {}
  print(db)
  for url in db.keys():
    html = db[url].decode()
    try:
      soup = bs4.BeautifulSoup(html, "html5lib")
      title = soup.find("h1", {"class" : "articleTtl"}) 
      if title is None: 
        continue

      print(title)
      time = soup.find("time", {"class":"articleDate"})
      body = soup.find("div", {"class":"articleBody"} )

      time = time.text
      titles = title.text.strip()
      bodies = body.text.strip()
      o = {"time":time, "titles":titles, "bodies":bodies }
      name = hashlib.sha256(url).hexdigest()
      open(f'contents/{name}', 'w').write( json.dumps(o, indent=2, ensure_ascii=False) )
    except Exception as ex:
      print(ex)
      continue

names = [ name for name in glob.glob('dbms/htmls_*.dbm') ]

#_map(names[0])
with concurrent.futures.ProcessPoolExecutor(max_workers=18) as exe:
  exe.map(_map, names)
