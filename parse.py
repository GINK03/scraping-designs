import glob

import bs4

import re
for name in glob.glob('htmls/*'):
  html = open(name).read() 
  soup = bs4.BeautifulSoup( html , 'html.parser' )
 
  try:
    contents  = " ".join( [p.text for p in soup.find('div', {'id': 'cmsBody'}).find_all('p')] )
  except Exception:
    continue
  contents  = re.sub(r'Reserved*?$', '', contents)

  print( contents )
