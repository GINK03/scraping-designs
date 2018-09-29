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
  import random
  import datetime
  def graph_access(url, acc, obj=None):
    query = f'https://graph.facebook.com/?id={url}&fields=og_object{{engagement}},engagement&access_token={acc}'
    r     = requests.get(query, proxies=proxy)
    fb_obj   = json.loads(r.text)
    tdatetime = datetime.datetime.now()
    eval_time = tdatetime.strftime('%Y-%m-%d %H:%M:%S')
    
    obj = {} if obj is None else obj
    obj['url']       = url
    obj[eval_time] = fb_obj
    if fb_obj.get('error'):
      print('error', fb_obj['error']['message'])
      print(fb_obj)
      if 'Cannot specify an empty identifier' == fb_obj['error']['message']:
        path.unlink()
        time.sleep(5.0)
        return
      time.sleep(30.0)
      return
    datum = json.dumps(obj, indent=2, ensure_ascii=False)
    print(datum) 
    open(f'facebook_score_v2/{url_hash}', 'w').write( datum )
    
  # make loop
  while True:
    for index, path in enumerate(Path('darturl_clean').glob('*')):
      key = index%len(accs)
      acc = accs[random.randint(0, len(accs)-1)]

      proxy = proxys[ index%len(proxys) ]
      print(acc)
      url   = path.open().read()
      url_hash = sha256(bytes(url,'utf8')).hexdigest() 
      if os.path.exists(f'facebook_score_v2/{url_hash}'):
        obj = json.load(Path(f'facebook_score_v2/{url_hash}').open())
        eval_times = [datetime.datetime.strptime(eval_time, '%Y-%m-%d %H:%M:%S') for eval_time in obj.keys() if eval_time != 'url']
        eval_times = sorted(eval_times) 
        now_datetime = datetime.datetime.now()

        delta_time = now_datetime - eval_times[-1]
        print(eval_times)
        # 三時間たびにスキャンする
        if delta_time.seconds > 3600 * 3:
          graph_access(url, acc, obj)
        else:
          continue
      else:
        graph_access(url, acc, None)
        ...
      
      time.sleep(1.5)

if '--clean' in sys.argv:
  for path in Path('./facebook_score_v2').glob('*'):
    obj = json.load(path.open())
    if obj.get('error') is not None:
      path.unlink()
    
  
