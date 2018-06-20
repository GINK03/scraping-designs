from pathlib import Path

from bs4 import BeautifulSoup as BS

from concurrent.futures import ProcessPoolExecutor as PPE
import json
from hashlib import sha256
names = [name for name in Path('htmls').glob('*')]

def pmap(name):
  soup = BS(name.open().read())
  url = soup.find('meta', property="og:url")

  if '/review/' not in url['content']:
    return
  print(soup.title)
  for review in soup.find_all('div', {'class':'review'}):
    point = review.find('strong').text
    text = review.find('h3').text + review.find('p').text 
    text = text.replace('※本文にネタバレがあります。 [ ▼クリックして本文を読む ]', '')
    obj = {'point':point, 'text':text}
    obj = json.dumps(obj, ensure_ascii=False)
    hash = sha256(bytes(obj,'utf8')).hexdigest()
    open(f'objs/{hash}', 'w').write( obj )
    print( point, text)

with PPE(max_workers=16) as exe:
  exe.map(pmap, names) 

