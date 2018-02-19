import glob

import json

import pickle

import gzip

import os

import hashlib

import re
names = set([name.split('/').pop() for name in glob.glob('hrefs/*')])

asins = set()
for name in names:
  print(name)
  try:
    obj = json.loads(open('hrefs/' + name).read())
  except:
    ...

  for url in obj:
    ents = url.split('/') 
    ents = filter(lambda x: len(x) == 10  and x[0] == 'B', ents)
    ents = list(ents)
    if ents == []:
      continue
    asin = ents.pop()
    asins.add(asin)
  if len(asins) >= 10000:
    obj = json.dumps( list(asins), indent=2 ) 
    ha = hashlib.sha256(bytes(obj,'utf8')).hexdigest()
    open(f'chunk/{ha}', 'w').write( obj ) 
    asins = set()
