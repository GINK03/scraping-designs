from pathlib import Path
import json
import MeCab
import re
import pandas as pd
m = MeCab.Tagger('-Owakati')

robjs = []
for path in Path('./json').glob('*'):
    print(path)
    try:
        obj = json.load(path.open())
    except Exception as ex:
        path.unlink()
    try:
        basic = obj['basic']
        jusho = basic['住所']
        yachin = re.sub(r'万円', '', basic['管理費等'])
        #print(jusho, yachin)
        country = m.parse(jusho).strip()[:3]
        yachin = float(yachin)
        robj = { 'country': country, 'yachin': yachin }
        robjs.append(robj)
    except Exception as ex:
        print(ex)

df = pd.DataFrame(robjs)

df.to_csv('lexical_parsed.csv', index=None)


