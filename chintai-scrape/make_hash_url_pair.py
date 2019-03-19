import glob
import json
import pickle
import gzip
import os
import hashlib
import re
names = set([name.split('/').pop() for name in glob.glob('hrefs/*')])

hash_url = {}
for name in names:
    print(name)
    try:
        obj = json.loads(open('hrefs/' + name).read())
    except Exception as ex:
        continue
    # [urls.add(re.sub(r'\?.*?$', '', url)) for url in obj if hashlib.sha256(
    #    bytes(url, 'utf8')).hexdigest() not in names]
    for url in obj:
        hash = hashlib.sha256(bytes(url, 'utf8')).hexdigest()
        hash_url[hash] = url

json.dump(hash_url, fp=open('hash_url.json', 'w'), indent=2)
