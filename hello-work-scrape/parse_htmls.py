import requests
import glob
from pathlib import Path
import gzip
from bs4 import BeautifulSoup
from hashlib import sha256
from concurrent.futures import ProcessPoolExecutor as PPE

Path('job_description_htmls').mkdir(exist_ok=True)
def get_detail_job_description(url):
    ha = sha256(bytes(url, 'utf8')).hexdigest()
    if Path(f'job_description_htmls/{ha}').exists():
        return
    r = requests.get(url)
    print(url)
    r.encoding = r.apparent_encoding 
    with open(f'job_description_htmls/{ha}', 'w') as fp:
        fp.write(r.text)

def parse_local_overview_job_list(path):
    fullUrls = []
    html = gzip.decompress(path.open('rb').read())
    soup = BeautifulSoup(html, 'lxml')
    for a in soup.find_all('a', {'id':'ID_link'}):
        fullUrl = 'https://www.hellowork.go.jp/servicef/' + a.get('href')
        fullUrls.append(fullUrl)
    return fullUrls

paths = [path for path in Path().glob('htmls/*')]
fullUrls = set()
with PPE(max_workers=8) as exe:
    for fullUrlsChunk in exe.map(parse_local_overview_job_list, paths):
        fullUrls |= set(fullUrlsChunk)
print('finish parse local overview job lists')
with PPE(max_workers=16) as exe:
    exe.map(get_detail_job_description, fullUrls)
