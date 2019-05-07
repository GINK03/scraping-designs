
from pathlib import Path
import gzip

files = list(Path('./jsons').glob('*'))
for idx, path in enumerate(files):
    #print(path)
    last_hash = str(path).split('/')[-1]
    if Path(f'htmls/{last_hash}').exists():
        print('exist', idx, len(files), last_hash)
        with Path(f'htmls/{last_hash}').open('wb') as fp:
            fp.write(gzip.compress(bytes('finish', 'utf8')))
    else:
        ...
