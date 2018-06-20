from pathlib import Path

import bs4

from concurrent.futures import ProcessPoolExecutor as PPE

paths = [path for path in Path('./htmls').glob('*')]

def pmap(path):
  soup = bs4.BeautifulSoup( path.open().read() )
  #print(soup)
  title = soup.title
  if 'ã' in str(title) or '429' in str(title) or '403' in str(title):
    print( title )
    path.unlink()

with PPE(max_workers=16) as exe:
  exe.map(pmap, paths)
