from tqdm import tqdm
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
import CONFIG

URL = 'https://profile.ameba.jp/'


def html(arg):
    key, urls = arg

    href_buffs = set()
    for idx, url in enumerate(urls):
        time.sleep(1)
        try:
            save_name = CONFIG.HTML_PATH_PROFILE + '/' + \
                hashlib.sha256(bytes(url, 'utf8')).hexdigest()[:20]
            save_href = CONFIG.HREF_PATH_PROFILE + '/' + \
                hashlib.sha256(bytes(url, 'utf8')).hexdigest()[:20]

            if Path(save_href).exists() is True:
                continue
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) [Scraper]'}
            print(key, idx, len(urls), url)
            try:
                r = requests.get(url, headers=headers)
            except Exception as e:
                continue
            r.encoding = 'UTF-8'  # r.apparent_encoding
            html = r.text
            try:
                open(save_name, 'wb').write(gzip.compress(bytes(html, 'utf8')))
            except OSError as ex:
                print('error write html', url)
                continue
            soup = bs4.BeautifulSoup(html, 'lxml')

            hrefs = []
            for href in soup.find_all('a', href=True):
                _url = href['href']
                try:
                    if '//' == _url[0:2]:
                        _url = 'https:' + _url
                except IndexError as e:
                    continue
                try:
                    if '/' == _url[0]:
                        _url = URL + _url
                except IndexError as e:
                    continue
                if re.search(r'profile.ameba.jp', _url) is None:
                    continue
                # print(_url)
                hrefs.append(_url)
            try:
                open(save_href, 'w').write(
                    json.dumps(list(set(hrefs) - href_buffs)))
                print('ordinal save href data', url)
            except Exception as ex:
                print('cannot save', url, ex)
                continue
        except Exception as ex:
            print(ex)

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
    html((-1, [URL]))
    while True:
        files = list(Path(CONFIG.HREF_PATH_PROFILE).glob('*'))
        urls = set()
        random.shuffle(files)
        for file in tqdm(files):
            [urls.add(url) for url in json.load(open(file))]
        with concurrent.futures.ProcessPoolExecutor(max_workers=16) as executor:
            args = chunk_up(urls)
            executor.map(html, args)

main()
