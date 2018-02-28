import gzip

import os

import glob

for name in glob.glob('htmls/*'):
  print(name)
  sha = name.split('/').pop()
  html = gzip.compress(bytes(open(name, 'r').read(),'utf8'))

  #open('../../sdb/' + sha, 'wb').write( html )

  #os.remove(name)
  open(name, 'wb').write(html)
