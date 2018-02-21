import glob

import bs4

import concurrent.futures

import os

import re

import json

import hashlib

import gzip
def _name(arr):
  index, names = arr

  for name in names:
    try:
      soup = bs4.BeautifulSoup( gzip.decompress(open(name, 'rb').read()) )

      reviews = soup.find_all('div', {'data-hook':'review'})
      if reviews == []:
        continue
      for review in reviews:
        star = review.find('i', {'data-hook':'review-star-rating'}).text
        body = review.find('span', {'data-hook':'review-body'}).text.strip()
        if re.search('5つ星', star) is None:
          '''エンコーディングがバグってる'''
          '''削除'''
          os.remove(name) 
          break
        star = float(re.search(r'5つ星のうち(.*?)$', star).group(1))
        d = {'star':star, 'body':body}
        obj = json.dumps(d, indent=2, ensure_ascii=False)
        sha = hashlib.sha256(bytes(obj,'utf8')).hexdigest() 
        open('reviews/' + sha, 'w').write(obj)
        print(obj)
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
