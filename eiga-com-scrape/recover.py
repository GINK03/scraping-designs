import glob

import json

import pickle

import gzip
names = set([name.split('/').pop() for name in glob.glob('hrefs/*')])

urls = set()
for name in names:
  print(name)
  obj = json.loads(open('hrefs/' + name).read())
  [urls.add(url) for url in obj if url not in names]

open('urls.pkl.gz', 'wb').write(gzip.compress(pickle.dumps(urls)))
