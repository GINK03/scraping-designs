import requests
import glob
import re
from pathlib import Path
from bs4 import BeautifulSoup
from hashlib import sha256
import gzip
import json
import random
def hashing(x):
    sha = sha256(bytes(x, 'utf8')).hexdigest()[:10]
    return sha

def save_html(url, text):
    sha = hashing(url)
    with open(f'htmls/{sha}', 'wb') as fp:
        fp.write(gzip.compress(bytes(text,'utf8')))

def is_exist_url(url):
    sha = hashing(url)
    return Path(f'htmls/{sha}').exists()

def save_href(hrefs):
    obj = json.dumps(json.dumps(list(hrefs))) 
    sha = hashing(obj)
    with open(f'hrefs/{sha}', 'w') as fp:
        fp.write(json.dumps(list(hrefs)))

def if_no_urls_then_fill_backup(urls):
    if len(urls) == 0:
        for fn in glob.glob('hrefs/*'):
            urls |= set(json.load(open(fn)))
        return urls
    else:
        return urls

def grab(arg):
    base_url = 'https://xn--pckua2a7gp15o89zb.com/'
    urls = [base_url]

    Path('hrefs').mkdir(exist_ok=True)
    Path('htmls').mkdir(exist_ok=True)
    while True:
        rurls = set()
        urls = if_no_urls_then_fill_backup(urls)
        #print(urls)
        for url in random.sample(list(urls), len(urls)):
            try:
                if is_exist_url(url):
                    continue
                r = requests.get(url)
                soup = BeautifulSoup(r.text)
                save_html(url, r.text)
                local_urls = set()
                for a in soup.find_all('a', {'href':True}):
                    href = a.get('href')
                    if re.search(r'^javascript', href) is not None:
                        continue
                    if len(href) >= 1 and href[0] == '/':
                        href = 'https://求人ボックス.com' + href
                    if re.search(r'^https://求人ボックス.com', href) is None and re.search(r'^https://xn--pckua2a7gp15o89zb.com', href) is None:
                        continue
                    if is_exist_url(href):
                        continue
                    print(href)
                    rurls.add(href)
                    local_urls.add(href)
                save_href(hrefs=local_urls)
            except Exception as ex:
                print(ex)
                exit()
        urls = rurls     

#grab(0)
#exit()
from concurrent.futures import ProcessPoolExecutor as PPE
with PPE(max_workers=16) as exe:
    exe.map(grab, list(range(16)))
