import pandas as pd


df = pd.read_csv('preds.csv')

hash_preds = {}
for row in df.to_dict('record'):
  #print(row)
  #print(row['_h2_'])
  hash_preds[row['_hashval_']] = row['preds']
import json
h2_hash = json.load(open('../h2_hash.json'))
hash_h2 = { hash:h2 for h2, hash in h2_hash.items() }


for hash, h2 in hash_h2.items():
  print(hash, h2, hash_preds.get(hash))
