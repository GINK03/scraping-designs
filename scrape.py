
# coding: utf-8
import os
import math
import sys
import urllib.request, urllib.error, urllib.parse
import http.client
import ssl
import re
import multiprocessing as mp
from socket import error as SocketError
import bs4
import concurrent.futures
import pickle

def html_fetcher(url):
  if url.status == True:
    return None
  if 'itmedia' not in url.url:
    return None
  if 'articles' not in url.url:
    return None
  if '.jpg' in url.url:
    return None
  print( url.url )
  html = None
  for _ in range(5):
    try:
      opener = urllib.request.build_opener()
      TIME_OUT = 5
      opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.63 Safari/537.36')]
      html = opener.open(url.url, timeout = TIME_OUT).read()
      pass
    except Exception as e:
      print( e )
      continue
    break
  if html == None:
    return None

  soup      = bs4.BeautifulSoup(html)
  title     = (lambda x:str(x.string) if x != None else 'Untitled')( soup.title ).replace(' - ITmedia NEWS.', '').replace('/', '')
  try:
    contents  = " ".join( [p.text for p in soup.find('div', {'id': 'cmsBody'}).find_all('p')] )
  except Exception as e:
    print( e )
    return None

  # JSを削除
  contents  = re.sub(r'Reserved*?$', '', contents)
  
  links = list(set([a['href'] for a in soup.find_all('a', href=True)]) )
  url.status = True 
  return title, contents, links, url.url

class URL:
  def __init__(self, url):
    self.url    = url
    self.status = False
def main():
  seed = 'http://www.itmedia.co.jp/news/articles/1707/06/news098.html'
  try:
    res =  html_fetcher(URL(seed)) 
    title, contents, links, url = res
    
    urls = set( map( lambda x: URL(x), links) )
    noneeds = set(seed)
    print( contents )
  except:
    ...
  try:
    noneeds = pickle.loads( open('noneeds.pkl', 'rb').read() )
    urls    = pickle.loads( open('urls.pkl', 'rb').read() )
  except:
    ...
  while True:
    nextUrls = set()
    #with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    #  for res in executor.map(html_fetcher, urls):
    for res in [html_fetcher(url) for url in urls]:
      if res is None:
         continue
      title, contents, links, url = res
      noneeds.add( url )
      try:
        open('download/{title}.txt'.format(title=title), 'w').write(contents)
      except OSError as e:
        ...
      [ nextUrls.add( URL(x) ) if x not in noneeds else None  for x in links ] 
    open('noneeds.pkl', 'wb').write( pickle.dumps(noneeds) )
    open('urls.pkl', 'wb').write( pickle.dumps(urls) )
    urls = nextUrls

       
main()
