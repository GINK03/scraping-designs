from pathlib import Path
import glob
from bs4 import BeautifulSoup 
import re
import mojimoji
import pandas as pd

def sanitize(x):
    x = re.sub(r'\s{1,}', ' ', x)
    x = x.strip()
    x = mojimoji.zen_to_han(x, kana=False)
    return x

objs = []
for path in list(Path().glob('job_description_htmls/*'))[:100]:
    soup = BeautifulSoup(path.open().read())
    obj = {}
    for tr in soup.find('div', {'class':'d-table'}).find_all('tr'):
        key = (sanitize(tr.find('th').text))
        val = (sanitize(tr.find('td').text))
        obj[key] = val
    print(obj)
    objs.append(obj)

df = pd.DataFrame(objs)
df.to_csv('local.csv', index=None)
