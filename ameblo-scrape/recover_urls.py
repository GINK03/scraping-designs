from pathlib import Path
import json
from tqdm import tqdm
import gzip
import pickle
import random
from concurrent.futures import ProcessPoolExecutor as PPE

def pmap(arg):
    key, files = arg
    objs = set()
    for idx, path in enumerate(files):
        #sha256 = str(path).split('/')[-1]
        #sha256s.add(sha256)
        if idx % 10000 == 0:
            print(key, idx, len(files), path)
        try:
            with path.open() as fr:
                obj = set(json.load(fr))
        except Exception as ex:
            path.unlink()
            continue
        try:
            with path.open('w') as fw:
                json.dump(list(obj - objs), fp=fw)
        except Exception as ex:
            print(ex)
            continue
        objs |= obj
    return objs

def run():
    files = list(Path('hrefs').glob('*'))
    random.shuffle(files) 
    files = files[:1000_0000]

    args = {}
    for idx, file in enumerate(files):
        key = idx%16
        if args.get(key) is None:
            args[key] = []
        args[key].append(file)
    args = [(key, files) for key, files in args.items()]
    objs = set()
    with PPE(max_workers=4) as exe:
        for _objs in exe.map(pmap, args):
            objs |= _objs

    print('total size', len(objs))
    with open('urls.pkl.gz', 'wb') as fp:
        fp.write(gzip.compress(pickle.dumps(objs)))

    for url in list(objs)[:100]:
        print(url)

if __name__ == '__main__':
    run()
