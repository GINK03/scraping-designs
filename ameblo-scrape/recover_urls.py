from pathlib import Path
import json
from tqdm import tqdm
import gzip
import pickle
import random
def run():
    sha256s = set()
    objs = set()
    files = list(Path('hrefs').glob('*'))
    random.shuffle(files) 
    for idx, path in enumerate(files):
        sha256 = str(path).split('/')[-1]
        sha256s.add(sha256)
        if idx >= 1000000:
            break
        print(idx, len(files), path)
        try:
            obj = set(json.load(path.open()))
        except Exception as ex:
            #print(ex)
            path.unlink()
            continue
        objs |= obj

    print('no filtered size', len(objs))
    objs -= sha256s
    print('total size', len(objs))
    with open('urls.pkl.gz', 'wb') as fp:
        fp.write(gzip.compress(pickle.dumps(objs)))

    for url in list(objs)[:100]:
        print(url)

if __name__ == '__main__':
    run()
