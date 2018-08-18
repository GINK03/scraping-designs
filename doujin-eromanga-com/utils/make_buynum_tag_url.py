import glob
import re
import json
import MeCab
import pandas as pd
import sys
tags = { tag for tag, hashs in json.load(open('tag_hashs.json')).items() }
m = MeCab.Tagger('-Owakati')

data = []
for fn in glob.glob('./data/*'):
  #print(fn)
  obj = json.load(open(fn))
  #print(obj)
  star = re.search(r'(\d|,){1,}', obj['star']).group(0).replace(',', '')
  star = int(star)
  text = obj['h1'] + obj['detail']
  words = set(m.parse(text).strip().split())
  words = { word for word in words if word in tags }
  #print(star, words)
  data.append( (star, words) )
# make dense 
words_set = set()
for datum in data: 
  star, words = datum
  for word in words:
    words_set.add( word )
word_index = { word:index for index, word in enumerate(words_set) }
print(word_index)

if '--source' in sys.argv:
  datasource = {'_stars_':[]} 

  for word in word_index.keys():
    datasource[word] = []

  for datum in data:
    star, words = datum
    datasource['_stars_'].append( star )
    for word, index in word_index.items():  
      if word not in words:
        datasource[word].append( 0 )
      else:
        datasource[word].append( 1 )
  df = pd.DataFrame( datasource )
  print( df.head() )
  df.to_csv('source.csv', index=None)

if '--target' in sys.argv:
  # test
  datatarget = { '_hashval_':[] }
  for word in word_index.keys():
    datatarget[word] = []
  for fn in sorted(glob.glob('../static_folder/*/*.json')):
    print(fn)
    hashval = fn.split('/')[2].replace('.json', '')
    print(hashval)
    datatarget['_hashval_'].append( hashval )
    obj = json.load(open(fn))
    _tags = set( obj['tags'] )
    print(_tags)
    for word, index in word_index.items():  
      if word not in _tags:
        datatarget[word].append( 0 )
      else:
        datatarget[word].append( 1 )
  dfT = pd.DataFrame( datatarget )
  print( dfT.head() )
  dfT.to_csv('target.csv', index=None)
