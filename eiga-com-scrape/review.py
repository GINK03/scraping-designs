from pathlib import Path

from bs4 import BeautifulSoup as BS

from concurrent.futures import ProcessPoolExecutor as PPE

names = [name for name in Path('htmls').glob('*')]

def pmap(name):
  soup = BS(name.open().read())
  url = soup.find('meta', property="og:url")

  if '/review/' not in url['content']:
    return
  print(soup.title)

with PPE(max_workers=16) as exe:
  exe.map(pmap, names) 

