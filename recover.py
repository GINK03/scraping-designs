import glob

files = glob.glob('links/*')
size = len(files)

urls = set()
for index, name in enumerate(files):
  print( 'now iter', index, '/', size)
  [urls.add(url) for url in open(name).read().split('\n')]

import gzip
import pickle

open( 'urls.pkl.gz', 'wb').write( gzip.compress( pickle.dumps(urls) ) )
