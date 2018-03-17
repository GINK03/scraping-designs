from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

import bs4

import concurrent.futures

import hashlib

from pathlib import Path

import gzip
import sys
import pickle
URL = 'http://mangamura.org'
def _map(arg):
  key, urls = arg
  options = Options()
  options.add_argument('--headless')
  options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36")

  driver = webdriver.Chrome(chrome_options=options,executable_path='/usr/bin/chromedriver')

  return_chunk = set()
  for url in urls:
    ha = hashlib.sha256(bytes(url, 'utf8')).hexdigest()
    if Path(f'htmls/{ha}').exists():
      continue
    print(url)
    try:
      driver.get(url)
      #driver.find_element_by_name("q").send_keys("Python3 Selenium Windows Chrome")
      #driver.find_element_by_name("q").send_keys(Keys.ENTER)
      html = driver.page_source
      Path(f'htmls/{ha}').open('wb').write( gzip.compress( bytes(html,'utf8') ) )
      soup = bs4.BeautifulSoup(html, 'lxml')
      for a in soup.findAll('a', href=True):
        url = a.get('href')
        if len(url) >= 2 and url[0] == '/':
          url = URL + url
        if URL not in url:
          continue
        #print(url)
        return_chunk.add(url)
    except Exception as ex:
      print(ex)
  driver.quit() 
  return return_chunk

urls = [(0, ['http://mangamura.org'])]
_map(urls[0])

if '--resume' in sys.argv:
  urls = pickle.loads(gzip.decompress(open('./urls.pkl.gz', 'rb').read()))
  nexts = {}
  for index, url in enumerate(urls):
    key = index%12 
    if nexts.get(key) is None:
      nexts[key] = []
    nexts[key].append( url )
  urls = [(key, urls) for key, urls in nexts.items()]

while urls != set():
  nextUrl = set()
  with concurrent.futures.ProcessPoolExecutor(max_workers=12) as exe:
    for chunk in exe.map(_map, urls):
      [nextUrl.add(url) for url in chunk]
    nexts = {}
    for index, url in enumerate(list(nextUrl)):
      key = index%12 
      if nexts.get(key) is None:
        nexts[key] = []
      nexts[key].append( url )
    urls = [(key, urls) for key, urls in nexts.items()]

