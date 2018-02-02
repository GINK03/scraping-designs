import dbm

import pickle

import math

db = dbm.open("14-wakati.dbm", "r")

term_freq = {}

doc_size = len(list(db.keys()))
for url in db.keys():
  obj = pickle.loads(db[url])
  titles = obj["titles"].split()
  bodies = obj["bodies"].split()
  terms = set()
  [terms.add(term) for term in titles]
  [terms.add(term) for term in bodies]

  for term in terms:
    if term_freq.get(term) is None:
      term_freq[term] = 0
    term_freq[term] += 1

term_idf = {}
for term in list(term_freq.keys()):
  term_idf[term] = math.log( doc_size/term_freq[term] )

for term, idf in sorted( term_idf.items(), key=lambda x:x[1]*-1):
  print(term, idf)

