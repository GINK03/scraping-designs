import os
import math
import sys
import urllib.request
import urllib.error
import urllib.parse
import requests
import http.client
import ssl
import re
import multiprocessing as mp
from socket import error as SocketError
import bs4
import concurrent.futures
import pickle
import os
import gzip
import random
import json
import re
import hashlib
import time
from pathlib import Path
try:
    os.mkdir('htmls')
    os.mkdir('hrefs')
except:
    ...
URL = 'https://ameblo.jp'


def html(arg):
    key, urls = arg

    href_buffs = set()
    for idx, url in enumerate(urls):
        try:
            url = url.replace('//ameblo.jp//ameblo.jp', '//ameblo.jp')
            url = re.sub(r'#.*?$', '', url)
            save_name = 'htmls/' + hashlib.sha256(bytes(url, 'utf8')).hexdigest()
            save_href = 'hrefs/' + hashlib.sha256(bytes(url, 'utf8')).hexdigest()
            if Path(save_href).exists() is True:
                continue
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'}
            print(key, idx, len(urls), url)
            try:
                r = requests.get(url, headers=headers)
            except Exception as e:
                continue
            r.encoding = 'UTF-8'  # r.apparent_encoding
            html = r.text
            try:
                open(save_name, 'wb').write(gzip.compress(bytes(html, 'utf8')))
            except OSError:
                continue
            soup = bs4.BeautifulSoup(html, 'lxml')

            hrefs = []
            for href in soup.find_all('a', href=True):
                _url = href['href']
                try:
                    if '/' == _url[0]:
                        _url = URL + _url
                except IndexError as e:
                    continue
                if re.search(r'^' + URL, _url) is None:
                    continue
                _url = re.sub(r'\?.*?$', '', _url)
                _url = re.sub(r'#.*?$', '', _url)
                _url = _url.replace('//ameblo.jp//ameblo.jp', '//ameblo.jp')
                hrefs.append(_url)
            open(save_href, 'w').write(json.dumps(hrefs))
            [href_buffs.add(href) for href in set(hrefs)]
        except Exception as ex:
            print(ex)
    Path('tmp').mkdir(exist_ok=True)
    with open(f'tmp/{key:02d}.pkl', 'wb') as fp:
        fp.write( pickle.dumps(href_buffs) )

def chunk_up(urls):
    urls = list(urls)
    random.shuffle(urls)
    args = {}
    for idx, url in enumerate(urls):
        key = idx % 16
        if args.get(key) is None:
            args[key] = []
        args[key].append(url)
    args = [(key, urls) for key, urls in args.items()]
    return args

def main():
    #seed = URL
    #urls = html((-1, seed))

    try:
        print('try to load pickled urls')
        urls = pickle.loads(gzip.decompress(open('urls.pkl.gz', 'rb').read()))
        print(urls)
        print('finished to load pickled urls')
    except FileNotFoundError as e:
        ...
    #while True:
    with concurrent.futures.ProcessPoolExecutor(max_workers=16) as executor:
        args = chunk_up(urls)
        executor.map(html, args)


main()
