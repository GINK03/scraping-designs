import pandas as pd
from pathlib import Path
import json

from concurrent.futures import ProcessPoolExecutor as PPE


args = {}
for idx, path in enumerate(Path('jsons').glob('*')):
    key = idx % 96
    if args.get(key) is None:
        args[key] = []
    args[key].append(path)
args = [(key, paths) for key,paths in args.items()]

Path('tmp').mkdir(exist_ok=True)
def pmap(arg):
    key, paths = arg
    records = []
    for idx, path in enumerate(paths):
        print(key, idx, len(paths), path)
        try:
            record = json.load(path.open())
            records.append(record)
        except Exception as ex:
            print(ex)
    df = pd.DataFrame(records)
    df.to_csv(f'tmp/ameblo_{key:03d}.csv', index=None)

with PPE(max_workers=16) as exe:
    exe.map(pmap, args)
