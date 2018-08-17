
from pathlib import Path
import json
import requests
from concurrent.futures import ProcessPoolExecutor as ppe
import os
import re
fps = [fp for fp in Path('parsed').glob('*')]
def pmap(fp):
  try:
    obj = json.load(fp.open())
    text, hash, img_url, num_clk, target, tags = obj
    if os.path.exists(f'imgs/{hash}.jpg'):
      return 
    print(fp)
    print(obj)
    if re.search(r'^http:', img_url):
      img_url = img_url
    else:
      img_url = 'http:' + img_url

    r = requests.get(img_url)
    print(img_url)
    print(r.status_code)
    if r.status_code == 200:
      img = r.content
      with open(f'imgs/{hash}.jpg', 'wb') as f:
        f.write( img )
  except Exception as ex:
    print(ex)
with ppe(max_workers=96) as exe:
  exe.map(pmap, fps)

