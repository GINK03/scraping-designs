import bs4

import MeCab

import dbm

import os

import pickle

import glob

import concurrent.futures

import hashlib

import json

import os
m = MeCab.Tagger("-Owakati")

def _map(arg):
  key,names = arg
  for name in names:
      save = name.split('/').pop()
      if os.path.exists(f'contents/{save}'):
        continue
      soup = bs4.BeautifulSoup(open(name).read(), "html5lib")
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
      save = name.split('/').pop()
      open(f'contents/{save}', 'w').write( json.dumps(o, indent=2, ensure_ascii=False) )

args = {}
for index, name in enumerate(glob.glob('htmls/*')):
  key = index%32
  if args.get(key) is None:
    args[key] = []
  args[key].append( name )
args = [(key,names) for key,names in args.items()]
#_map(args[0])
with concurrent.futures.ProcessPoolExecutor(max_workers=18) as exe:
  exe.map(_map, args)
