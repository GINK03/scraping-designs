import glob

import bs4

import re

import os

import concurrent.futures 

def _map(name):

  save_name = 'texts/' + name.split('/').pop()
  link_name = 'links/' + name.split('/').pop()
  if os.path.exists(save_name) is True:
    return 
  html = open(name).read() 
  soup = bs4.BeautifulSoup( html , 'html.parser' )

  links = []
  for a in soup.find_all('a', href=True):
    link = a['href']
    try:
      if link[0] == '/':
        link = 'http://wwww.itmedia.co.jp' + link
    except:
      continue
    links.append( link )
  l = open(link_name, 'w')
  for link in links:
    l.write( link + '\n' )
    
  try:
    contents  = " ".join( [p.text for p in soup.find('div', {'id': 'cmsBody'}).find_all('p')] )
  except Exception:
    return
  contents  = re.sub(r'Reserved*?$', '', contents)

  print( name )
  open(save_name,'w').write( contents )

names = [name for name in glob.glob('htmls/*')]
with concurrent.futures.ProcessPoolExecutor(max_workers=16) as exe:
  exe.map(_map, names)
