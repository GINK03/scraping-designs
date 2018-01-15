import glob

import bs4

import concurrent.futures

import os

import re

import json

import hashlib

import re

import dbm
def _name(arr):
  index, names = arr
  db = dbm.open('dbms/{:09d}.db'.format(index), 'c')
  for name in names:
    soup = bs4.BeautifulSoup(open(name).read())
    #print(name)
    link = soup.find('link', {'rel':'canonical'})
    if link is None:
      continue
    href = link.get('href')
    #print(href)
    try:
      if re.search(r'^https://review.rakuten.co.jp', href) is None:
        continue
    except Exception as ex:
      print(ex)
      continue

    for review in soup.find_all('div', {'class':'revRvwUserMain'}):
      star = review.find('span', {'class':'revUserRvwerNum'})
      body = review.find('dd', {'class':'revRvwUserEntryCmt description'})
      #print(review)
      #print(body)
      if body is None:
        continue
      if star is None:
        continue
      d = {'star':star.text, 'body':body.text}
      obj = json.dumps(d, indent=2, ensure_ascii=False) 
      print(obj)
      try:
        sha256 = hashlib.sha256(bytes(obj, 'utf8')).hexdigest()
        #open('reviews/' + sha256, 'w').write( obj )
        db[ sha256 ] = obj
      except Exception as ex:
        print(ex)


arr = {}
for index, name in enumerate(glob.glob('htmls/*')):
  key = index%32
  if arr.get(key) is None:
    arr[key] = []
  arr[key].append(name)
arr = [(index,names) for index,names in arr.items()]
#_name(arr[0])
with concurrent.futures.ProcessPoolExecutor(max_workers=32) as exe:
  exe.map(_name, arr)
