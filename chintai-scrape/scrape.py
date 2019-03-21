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
import glob
import pickle
import os
import gzip
import random
import json
import re
import hashlib
import time
import logging
import sys

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
# create a file handler
handler = logging.FileHandler('work.log')
handler.setLevel(logging.INFO)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

hander_stdout = logging.StreamHandler(sys.stdout)
hander_stdout.setLevel(logging.INFO)
hander_stdout.setFormatter(formatter)
logger.addHandler(hander_stdout)
logger.addHandler(handler)

try:
    os.mkdir('htmls')
    os.mkdir('hrefs')
except:
    ...


def html(arg):
    key, urls = arg
    ret_urls = set()
    for url in urls:
        try:
            url = re.sub(r'/inquiry', '', url)
            save_name = 'htmls/' + \
                hashlib.sha256(bytes(url, 'utf8')).hexdigest()
            save_href = 'hrefs/' + \
                hashlib.sha256(bytes(url, 'utf8')).hexdigest()
            if os.path.exists(save_href) is True:
                continue
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:58.0) Gecko/20100101 Firefox/58.0'}
            headers['referer'] = 'https://www.amazon.co.jp'
            try:
                r = requests.get(url, headers=headers)
            except Exception as ex:
                print(ex)
                continue
            logger.info(f'{url} {r.status_code}')
            r.encoding = r.apparent_encoding
            html = r.text
            open(save_name, 'wb').write(gzip.compress(bytes(html, 'utf8')))
            soup = bs4.BeautifulSoup(html, 'lxml')
            ret_urls_chunk = set()
            for a in soup.find_all('a', href=True):
                urlNext = a['href']
                if urlNext is None:
                    continue
                if len(urlNext) >= 1 and urlNext[0] == '/':
                    urlNext = URL + urlNext
                if re.search(r'(#|javascript)', urlNext):
                    continue
                if re.search(f'^{URL}', urlNext) is None:
                    continue
                urlNext = re.sub(r'\?.*$', '', urlNext)
                assert urlNext != None, "illigal href"
                urlNext = re.sub(r'/inquiry', '', urlNext)
                assert re.match(
                    r'/inquiry', urlNext) is None, "this domain's exception"
                save_href_next = 'hrefs/' + \
                    hashlib.sha256(bytes(urlNext, 'utf8')).hexdigest()
                if os.path.exists(save_href_next) is True:
                    continue
                # print(urlNext)
                ret_urls_chunk.add(urlNext)
            with open(save_href, 'w') as fp:
                fp.write(json.dumps(list(ret_urls_chunk)))
            ret_urls |= ret_urls_chunk
        except Exception as ex:
            logger.info(f'{ex}')
    return ret_urls


URL = 'https://www.chintai.net'


def chunker(urls):
    args = {}
    for idx, url in enumerate(urls):
        key = idx % 50
        if args.get(key) is None:
            args[key] = []
        args[key].append(url)
    args = [(key, urls) for key, urls in args.items()]
    return args


def main():
    urls = html((0, [URL]))
    if urls is None or urls == set():
        urls = pickle.load(open('urls.pkl', 'rb'))
    while urls != set():
        next_urls = set()
        args = chunker(urls)
        # html(args[0])
        with concurrent.futures.ProcessPoolExecutor(max_workers=50) as executor:
            for urls in executor.map(html, args):
                if urls is None:
                    continue
                for url in urls:
                    next_urls.add(url)
        with open('urls.pkl', 'wb') as fp:
            fp.write(pickle.dumps(next_urls))
        urls = next_urls


main()
