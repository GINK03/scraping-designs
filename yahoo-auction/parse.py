
from pathlib import Path
from bs4 import BeautifulSoup as BS
import gzip
import re
from concurrent.futures import ProcessPoolExecutor as PPE

def pmap(arg):
  index, path, size = arg
  html = gzip.decompress(path.open('rb').read()).decode()
  soup = BS(html, 'html.parser')
  
  print(index, size, soup.title.text)
  wraps =  soup.find_all('tr') 

  objs = []
  for wrap in wraps:
    if wrap.find('h3') is None:
      continue
    description = wrap.find('h3').text.strip().replace('\n','').replace('\xa0', '')
    
    price    = re.search(r'(\d{1,})円', wrap.find('td', {'class':'pr1'} ).text.strip().replace(',','')).group(1)
    decision = wrap.find('td', {'class':'pr2'} ).text.strip()
    bit_num  = wrap.find('td', {'class':'bi'} ).text.strip() 
    last_day = wrap.find('td', {'class':'ti'} ).text.strip() 
    category = wrap.find('p', {'class':'com_slider'} ).text.strip().replace('\n', '').replace('\xa0', '').replace('カテゴリ', '')

    obj = { 'category':category, 'price':price, 'decision':decision, 'bit_num':bit_num, 'last_day':last_day }
    objs.append(obj)
  return objs
  #print(html)
paths = [path for path in Path('./htmls').glob('*')]
size = len(paths)
args = [(index, path, size) for index, path in enumerate(paths)]

#[pmap(arg) for arg in args]

objs = []
with PPE(max_workers=12) as exe:
  for _objs in exe.map(pmap, args):
    [objs.append(obj) for obj in _objs]
import pandas as pd
df = pd.DataFrame(objs)
df.to_csv('out.csv', index=None)
