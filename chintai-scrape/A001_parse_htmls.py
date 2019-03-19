import glob
import bs4 

import gzip
import pickle
import re
import os
from concurrent.futures import ProcessPoolExecutor as PPE

def pmap(arg):
    fn = arg
    html = gzip.decompress(open(fn, 'rb').read())
    soup = bs4.BeautifulSoup(html, 'html5lib')
    canonical = soup.find('link', {'rel':'canonical'})['href']
    print(soup.title.text, canonical)
    detail_table = soup.find('table', {'class':'bukken_detail_table'})
    detail_obj = {tr.text:td.text for tr, td in zip(detail_table.find_all('tr'), detail_table.find_all('td'))}
    print(detail_obj)
fns = [fn for fn in glob.glob('./htmls/*')]
with PPE(max_workers=32) as exe:
    exe.map(pmap, fns)
