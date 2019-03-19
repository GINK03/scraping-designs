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


def html(url):
    try:
        save_name = 'htmls/' + hashlib.sha256(bytes(url, 'utf8')).hexdigest()
        save_href = 'hrefs/' + hashlib.sha256(bytes(url, 'utf8')).hexdigest()
        if os.path.exists(save_href) is True:
            return
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:58.0) Gecko/20100101 Firefox/58.0'}
        headers['referer'] = 'https://www.amazon.co.jp'
        try:
            r = requests.get(url, headers=headers)
        except Exception as ex:
            print(ex)
            return
        logger.info(f'{url} {r.status_code}')
        r.encoding = r.apparent_encoding
        html = r.text
        open(save_name, 'wb').write(gzip.compress(bytes(html, 'utf8')))
        soup = bs4.BeautifulSoup(html, 'html5lib')

        ret_urls = set()
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
            save_href_next = 'hrefs/' + hashlib.sha256(bytes(urlNext, 'utf8')).hexdigest() 
            if os.path.exists(save_href_next) is True:
                continue
            #print(urlNext)
            ret_urls.add(urlNext)
        with open(save_href, 'w') as fp:
            fp.write(json.dumps(list(ret_urls)))
        return ret_urls
    except Exception as ex:
        logger.info(f'{ex}')
        return


URL = 'https://www.chintai.net'

def main():
    urls = html(URL)
    if urls is None:
        urls = pickle.load(open('urls.pkl', 'rb'))
    while urls != set():
        next_urls = set()
        with concurrent.futures.ProcessPoolExecutor(max_workers=256) as executor:
            for urls in executor.map(html, urls):
                if urls is None:
                    continue
                for url in urls:
                    next_urls.add(url)
        with open('urls.pkl', 'wb') as fp:
            fp.write(pickle.dumps(next_urls))
        urls = next_urls
main()
