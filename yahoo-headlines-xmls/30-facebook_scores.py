import requests
import json
from pathlib import Path
from hashlib import sha256
import os
import sys
import time
from datetime import datetime 
accs = [ line.strip() for line in open('tokens') ]

proxys = [ {'http':f'http://{es[0]}:{es[1]}'} for es in [ line.strip().split() for line in open('proxys') ] ]
print(proxys)
if '--scan' in sys.argv:
  # make loop

  #while True:
  for index, path in enumerate(Path('./darturl_clean').glob('*')):
    key = index%len(accs)
    acc = accs[key]

    proxy = proxys[ index%len(proxys) ]
    print(acc)
    url   = path.open().read()
    url_hash = sha256(bytes(url,'utf8')).hexdigest() 
    if os.path.exists(f'facebook_score/{url_hash}'):
      continue
    query = f'https://graph.facebook.com/?id={url}&fields=og_object{{engagement}},engagement&access_token={acc}'
    r     = requests.get(query, proxies=proxy)
    obj   = json.loads(r.text)
    obj['url'] = url
    tdatetime = datetime.now()
    eval_time = tdatetime.strftime('%Y-%m-%d %H:%M:%S')
    obj['eval_time'] = eval_time
    if obj.get('error'):
      print('error', obj['error']['message'])
      print(obj)
      if 'Cannot specify an empty identifier' == obj['error']['message']:
        path.unlink()
        time.sleep(5.0)
        continue
      time.sleep(35.0)
      continue
    datum = json.dumps(obj, indent=2, ensure_ascii=False)
    print(datum) 
    open(f'facebook_score/{url_hash}', 'w').write( datum )
    time.sleep(1.5)

if '--clean' in sys.argv:
  for path in Path('./facebook_score').glob('*'):
    obj = json.load(path.open())
    if obj.get('error') is not None:
      path.unlink()
    
  
