
from pathlib import Path

import gzip

from bs4 import BeautifulSoup as BS

from concurrent.futures import ProcessPoolExecutor as PPE

shared_paths = {} 
for index, path in enumerate(list(Path("./htmls/").glob("*"))):#[:10000]):
  key = index%10
  if shared_paths.get(key) is None:
    shared_paths[key] = []
  shared_paths[key].append( path )

args = [ (key, paths) for key, paths in shared_paths.items() ]

def pmap(arg):
  key, paths = arg
  srcs = set()
  size = len(paths)

  for nu, path in enumerate(paths):
    html = gzip.decompress(path.open('rb').read()).decode('utf8')
    soup = BS(html)

    print(key, nu, size, path)
    for img in soup.findAll("img"):
      src = img["src"]
      if src not in srcs:
        srcs.add(src)
  return srcs

#pmap(args[0])
srcs = set()
with PPE(max_workers=10) as exe:
  for _srcs in exe.map(pmap, args):
    srcs = srcs | _srcs

import json
json.dump(list(srcs), fp=open('img_urls.json', 'w'), indent=2)
