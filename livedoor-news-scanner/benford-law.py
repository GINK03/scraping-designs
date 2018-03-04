
from pathlib import Path

import json

import re

head_freq = {}
for name in Path('./contents').glob('*'):
  obj = json.load(name.open())
  heads = [ f'{int(num)}'[0] for num in re.findall(r'\d{1,}', obj['bodies']) ]
  #print(heads)
  for head in heads:
    if head_freq.get(head) is None:
      head_freq[head] = 0
    head_freq[head] += 1

for head, freq in sorted(head_freq.items(), key=lambda x:x[1]*-1):
  print(head, freq)
