
from pathlib import Path
from bs4 import BeautifulSoup
from concurrent.futures import ProcessPoolExecutor
import re
import requests
from hashlib import sha256
import os

def trim(x):
  return re.sub(r'\s', '',x)
def pmap(arg):
  path = arg 
  res = {}
  soup = BeautifulSoup(path.open().read())
  iters = soup.find_all('div', {'class':'dlist'})
  if iters == []:
    return
  
  # 事件番号
  dlist0 = iters[0]
  mini_blocks = dlist0.find_all('div', {'class':None})
  f,v = map(lambda x:trim(x.text), mini_blocks[0].find_all('div'))
  res[f] = v
  case_number = v

  # 結果
  dlist0 = iters[0]
  mini_blocks = dlist0.find_all('div', {'class':None})
  f,v = map(lambda x:trim(x.text), mini_blocks[5].find_all('div'))
  res[f] = v

  # 判決事項
  dlist2 = iters[2]
  mini_blocks2 = dlist2.find_all('div', {'class':None})
  f,v = map(lambda x:trim(x.text), mini_blocks2[0].find_all('div'))
  res[f] = v

  # 全文 
  dlist2 = iters[2]
  mini_blocks2 = dlist2.find_all('div', {'class':None})
  f,v = map(lambda x:x, mini_blocks2[3].find_all('div'))
  f = trim(f.text)
  v = v.find('a').get('href')
  res[f] = v
  url = 'http://www.courts.go.jp' + v
  # pdfをダウンロード
  if not Path(f'pdfs/{case_number}.pdf').exists():
    os.system(f'wget {url} -O pdfs/"{case_number}".pdf') 
  #text = os.popen(f'pdftotext pdfs/"{case_number}".pdf -').read()
  #print(text)
  print(res)

args = []
for path in Path('./htmls').glob('*'):
  args.append(path)

pmap(args[0])
with ProcessPoolExecutor(max_workers=16) as exe:
  exe.map(pmap, args)
