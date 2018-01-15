import glob

import dbm

import json
for name in glob.glob('dbms/*.db'):
  db = dbm.open(name)
  for key in db.keys():
    obj = json.loads( db[key].decode() )
    print(obj)
