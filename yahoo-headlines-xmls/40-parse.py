
from pathlib import Path
import gzip
from bs4 import BeautifulSoup as BS
for path in Path('./htmls').glob('*'):
  a = gzip.decompress(path.open('rb').read()).decode()
  soup = BS(a, 'html.parser')
  try:
    print(soup.find('p', {'class':'ynDetailText yjDirectSLinkTarget'}).text)
  except Exception as ex:
    print(ex)
    ...
