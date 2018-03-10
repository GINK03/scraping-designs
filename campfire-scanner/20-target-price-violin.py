import bs4

import lxml

import MeCab

import dbm

import os

import pickle

import glob

import concurrent.futures

import hashlib

import json

import os

import re
m = MeCab.Tagger("-Owakati")

def _map(arg):
  key,names = arg

  results = []
  for name in names:
    save = name.split('/').pop()
    if os.path.exists(f'contents/{save}'):
      continue
    soup = bs4.BeautifulSoup(open(name).read(), "lxml")

    number = soup.find('strong', {'class':'number'})
    if number is None:
      continue

    bar = soup.find('div', {'class':'bar'})
    target = soup.find('div', {'class':'target'})
    sub = soup.find('div', {'class':'subtitle'})
    
    try:
      profile, category = sub.find_all('a')
    except:
      continue
    #print(number)
    #print(bar)
    #print(target)
    #print(category)

    try:
      number = re.search(r'\d{1,}', number.text.replace(',', '')).group(0)
      target = re.search(r'\d{1,}', target.text.replace(',', '')).group(0)
      category = category.text.replace(',', '')
    except:
      continue
    #print(number, target, category)
    result = (number, target, category)
    results.append(result)
  return results
  #o = {"time":time, "titles":titles, "bodies":bodies }
  #save = name.split('/').pop()
  #open(f'contents/{save}', 'w').write( json.dumps(o, indent=2, ensure_ascii=False) )


args = {}
for index, name in enumerate(glob.glob('htmls/*')):
  key = index%32
  if args.get(key) is None:
    args[key] = []
  args[key].append( name )
args = [(key,names) for key,names in args.items()]
#_map(args[0])

results = []
with concurrent.futures.ProcessPoolExecutor(max_workers=18) as exe:
  for _results in exe.map(_map, args):
    for result in _results:
      results.append(result)

pickle.dump(results, open('results.pkl', 'wb'))
  
