import requests

from bs4 import BeautifulSoup as BS
import re
from hashlib import sha256
import json

r = requests.get('https://headlines.yahoo.co.jp/rss/list')

soup = BS(r.text)

xmls = []
for link in soup.find_all('link'):
  href = link.get('href')
  if re.search(r'xml$', href) is None:
    continue
  xmls.append(href)


for a in soup.find_all('a'):
  href = a.get('href')
  if re.search(r'xml$', href) is None:
    continue
  xmls.append(href)

#print(xmls)

def pmap_xml(arg):
  xml = arg
  r = requests.get(xml)
  soup = BS(r.text, 'html.parser')
  for item in soup.find_all('item'):
    try:
      title = item.find('title').text
      pubdate = item.find('pubdate').text
      link = [ field for field in str(item).split('\n') if '<link/>' in field ][0].replace('<link/>', '')
      
      obj = {'title':title, 'pubdate':pubdate, 'link':link}
      obj['link_hash'] = sha256(bytes(link, 'utf8')).hexdigest()  
      datum = json.dumps( obj , indent=2, ensure_ascii=False)
      hashval = sha256(bytes(datum, 'utf8')).hexdigest()
      open(f'xml_parse/{hashval}', 'w').write( datum )
      print(obj)
    except Exception as ex:
      print(ex)
from concurrent.futures import ProcessPoolExecutor as PPE
with PPE(max_workers=10) as exe:
  exe.map(pmap_xml, xmls)
