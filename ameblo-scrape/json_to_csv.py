import pandas as pd
from pathlib import Path
import json

records = []
paths = list(Path('jsons').glob('*'))
for idx, path in enumerate(paths):
    print(idx, len(paths), path)
    try:
        record = json.load(path.open()) 
        records.append(record)
    except Exception as ex:
        print(ex)

df = pd.DataFrame(records)
df.to_csv('ameblo.csv', index=None)
