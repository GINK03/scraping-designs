import requests
import json
from pathlib import Path
from hashlib import sha256
import os
import time
acc = os.environ['FACEBOOK_ACC']
for path in Path('./darturl_clean').glob('*'):
  url   = path.open().read()
  url_hash = sha256(bytes(url,'utf8')).hexdigest() 
  if os.path.exists(f'facebook_score/{url_hash}'):
    continue
  query = f'https://graph.facebook.com/?id={url}&fields=og_object{{engagement}},engagement&access_token={acc}'
  r     = requests.get(query)
  obj   = json.loads(r.text)
  obj['url'] = url
  if obj.get('error'):
    continue
 
  datum = json.dumps(obj, indent=2, ensure_ascii=False)
  print(datum) 
  open(f'facebook_score/{url_hash}', 'w').write( datum )
  time.sleep(1.5)
