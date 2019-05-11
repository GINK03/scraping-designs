import os
import sys
import glob
import gzip
import bs4
import lxml
import concurrent.futures
import re
from pathlib import Path
import json
import random
import CONFIG


def pmap(arg):
    key, names = arg
    random.shuffle(names)
    for name in names:
        try:
            sha256 = name.split('/')[-1]
            if Path(f'jsons_profile/{sha256}').exists():
                continue
            print(name)
            html = gzip.decompress(open(name, 'rb').read()).decode()
            soup = bs4.BeautifulSoup(html, 'lxml')
            for script in soup(["script", "style"]):
                script.extract()    # rip it out

            canonical = soup.find('link', {'rel': 'canonical'})
            if canonical is None:
                Path(name).unlink()
                continue
            canonical = canonical.get('href')
            user = re.search(r'https://profile.ameba.jp/ameba/(.*?)$', canonical)
            if user is None:
                Path(name).unlink()
                continue
            user = user.group(1)
            term_value = {}
            for user_info_list in soup.find_all('dl', {'class':'user-info__list'}):
                term = user_info_list.find('dt', {'class':'user-info__term'}).text
                value = user_info_list.find('dd', {'class':'user-info__value'}).text
                term_value[term] = value
            record = {}
            record.update(term_value)
            record['user'] = user
            with open(f'jsons_profile/{sha256}', 'w') as fp:
                fp.write(json.dumps(record, indent=2, ensure_ascii=False))
            if random.random() <= 0.05:
                print(record)
        except Exception as ex:
             Path(name).unlink()
             print(ex)


def main():
    args = {}
    for index, name in enumerate(glob.glob(CONFIG.HTML_PATH_PROFILE + '/*')):
        key = index % 32
        if args.get(key) is None:
            args[key] = []
        args[key].append(name)
    args = [(key, names) for key, names in args.items()]
    #[pmap(arg) for arg in args]
    with concurrent.futures.ProcessPoolExecutor(max_workers=32) as exe:
        exe.map(pmap, args)


if __name__ == '__main__':
    if '--loop' in sys.argv:
        while True:
            main()
    else:
        main()
