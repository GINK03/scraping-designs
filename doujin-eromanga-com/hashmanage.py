import glob
from hashlib import sha256
import json
import os

def pmap(fn):
  try:
    name = fn.split('/').pop()
    imgs = [( index, open(f,'rb').read() ) for index, f in enumerate(sorted(glob.glob(fn+'/*.jpg')))]
    try:
      obj = json.load( open([ f for f in glob.glob(fn+'/*.json') ][-1] ) )
    except: 
      print('json is not exists')
      return
    hash256 = sha256(bytes(name,'utf8')).hexdigest()
    try:
      os.mkdir('static_folder/'+ hash256)
    except:
      print('already processed')
      return
    print(obj)
    base = 'static_folder/'+ hash256
    for i, img in imgs:
      open(base + f'/{i:04d}.jpg', 'wb' ).write( img )
    open(base + '/' +'obj.json', 'w').write(json.dumps(obj) ) 
  except Exception as ex:
    print(ex)


from concurrent.futures import ProcessPoolExecutor as PPE
fns = [fn for fn in glob.glob('folders/*')]

with PPE(max_workers=128) as exe:
  exe.map(pmap, fns)
