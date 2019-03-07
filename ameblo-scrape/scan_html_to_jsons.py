import os
import glob
import gzip
import bs4, lxml
import concurrent.futures
import re
import hashlib
from pathlib import Path
import json
def _map(arg):
    index, name = arg
    try:
        sha256 = name.split('/')[-1] 
        if Path(f'jsons/{sha256}').exists():
            return
        html = gzip.decompress(open(name, 'rb').read()).decode()
        soup = bs4.BeautifulSoup(html, 'lxml')
        for script in soup(["script", "style"]):
            script.extract()    # rip it out

        article = soup.find('article')
        if article is None:
            Path(name).unlink()
            return
        titles = [article.h1, article.h2] 
        if titles == [None, None]:
            return
        title = [t for t in [t.text for t in titles if t is not None] if t not in ['SNSアカウント']]
        title = ' '.join(title)
        canonical = soup.find('link', {'rel':'canonical'})
        if canonical is None:
            Path(name).unlink()
            return
        time = soup.time.get('datetime')
        body = soup.find('div', {'id':'entryBody'})
        if body is None:
            Path(name).unlink()
            return
        body = body.text.replace('\n', ' ')
        body = re.sub(r'\s{1,}', ' ', body)
        record = {'title':title, 'canonical':canonical.get('href'), 'time':time, 'body':body, 'sha256':sha256}
        with open(f'jsons/{sha256}', 'w') as fp:
            fp.write(json.dumps(record, indent=2, ensure_ascii=False))
        print(record)
    except Exception as ex:
        print(ex)

args = [(index,name) for index,name in enumerate(glob.glob('htmls/*'))]
with concurrent.futures.ProcessPoolExecutor(max_workers=64) as exe:
  exe.map( _map, args)
