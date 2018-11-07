import os
import glob
import gzip
import bs4, lxml
import concurrent.futures
import re
import hashlib
import json
def _map(arg):
  index, name = arg
  print(name)
  html = gzip.decompress(open(name, 'rb').read()).decode()
  soup = bs4.BeautifulSoup(html, 'html5lib')

  for script in soup(["script", "style"]):
    script.extract()    # rip it out
  
  #for d in soup.find_all('div'):
  #   print(d)
  if soup.find('dl', {'class':'thread'}) is None:
    return

  dts = soup.find('dl', {'class':'thread'}).find_all('dt')
  dds = soup.find('dl', {'class':'thread'}).find_all('dd')
  for dt,dd in zip(dts,dds):
    try:
      user = dt.find('b').text
      datetime = re.search(r'\d\d\/\d\d/\d\d', dt.text).group(0)
      post = re.sub(r'\n', ' ', dd.text)
      obj = {'user':user, 'datetime':datetime, 'post':post}
      ser = json.dumps(obj, indent=2, ensure_ascii=False)
      hashed = hashlib.sha256(bytes(ser, 'utf8')).hexdigest()
      open(f'posts/{hashed}.json', 'w').write( ser )
      #print(user, datetime, post)
    except Exception as ex:
      print(ex)
      print(dt.text)

args = [(index,name) for index,name in enumerate(glob.glob('htmls/*'))]
[_map(arg) for arg in args]
with concurrent.futures.ProcessPoolExecutor(max_workers=16) as exe:
  exe.map( _map, args)
