import json
from pathlib import Path
import glob
import pandas as pd

objs = []
for idx, path in enumerate(Path().glob('./job_description_jsons/*')):
    print(idx)
    obj = json.load(path.open())
    objs.append(obj)

df = pd.DataFrame(objs)
print('raw size', len(df))
df.drop(['所在地'], axis=1).to_csv('raw.csv', index=None)
df = df[pd.notnull(df['所在地'])]
print('filter size', len(df))
df.to_csv('local.csv', index=None)
