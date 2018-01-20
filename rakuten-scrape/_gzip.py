import gzip

import os

import glob

import concurrent.futures

def _map(arr):
  index, names = arr
  for name in names:
    c = open(name, 'rb').read()
    try:
      gzip.decompress(c)
    except Exception as ex:
      print(ex)
      s = gzip.compress(c)
      open(name, 'wb').write(s)

arrs = {}
for index, name in enumerate(glob.glob('./htmls/*')):
  key = index%36
  if arrs.get(key) is None:
    arrs[key] = []
  arrs[key].append( name )

arrs = [(key, names) for key, names in arrs.items()]
with concurrent.futures.ProcessPoolExecutor(max_workers=32) as exe:
  exe.map(_map, arrs)

