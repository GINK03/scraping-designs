import glob

import bs4

import re

import os

import concurrent.futures 

def _map(name):

  save_name = 'texts/' + name.split('/').pop()
  if os.path.exists(save_name) is True:
    return 
  html = open(name).read() 
  soup = bs4.BeautifulSoup( html , 'html.parser' )
 
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
