import dbm

import pickle

import datetime
db = dbm.open('14-wakati.dbm', 'r')

day_values = {}
for key in db.keys():
  obj = pickle.loads( db[key] )
  dtime = datetime.datetime.strptime(obj['time'], "%Y年%m月%d日 %H時%M分") # 2017年12月26日 15時51分
  #print(dtime)
  day = dtime.strftime("%Y-%m-%d")
  if day_values.get(day) is None:
    day_values[day] = []
  day_values[day].append( obj )

for day, values in sorted( day_values.items(), key=lambda x:x[0]):
  print(day, len(values))
