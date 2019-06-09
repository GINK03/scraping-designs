from pathlib import Path
import glob
from bs4 import BeautifulSoup 
import re
import mojimoji
import pandas as pd
from tqdm import tqdm
import json
def sanitize(x):
    x = re.sub(r'\s{1,}', ' ', x)
    x = x.strip()
    x = mojimoji.zen_to_han(x, kana=False)
    return x

paths = list(Path().glob('job_description_htmls/*'))
Path(f'job_description_jsons').mkdir(exist_ok=True)
for idx, path in tqdm(enumerate(paths)):
    last_fn = str(path).split('/')[-1]
    if Path(f'job_description_jsons/{last_fn}').exists():
        continue
    try:
        soup = BeautifulSoup(path.open().read())
        obj = {}
        for tr in soup.find('div', {'class':'d-table'}).find_all('tr'):
            key = (sanitize(tr.find('th').text))
            val = (sanitize(tr.find('td').text))
        obj[key] = val
        json.dump(obj, fp=open(f'job_description_jsons/{last_fn}', 'w'), indent=2, ensure_ascii=False)
    except Exception as ex:
        print(ex)
    #print(obj)
    #objs.append(obj)

#df = pd.DataFrame(objs)
#df.to_csv('local.csv', index=None)
