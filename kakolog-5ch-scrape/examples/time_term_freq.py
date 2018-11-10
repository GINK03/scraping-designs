from pathlib import Path
import json
from concurrent.futures import ProcessPoolExecutor as PPE

import smart_open

def pmap(arg):
	key,path = arg
	date_freq = {}
	print(path)
	fp = open(path)
	try:
		for line in fp:
			line = line.strip()	
			try:
				obj = json.loads(line)
			except: 
				continue
			datetime = obj['datetime']
			datetime = '20' + '/'.join(datetime.split('/')[0:2])
			post = obj['post']
			#print(datetime, line)
			if len(datetime) != 7:
				continue
			if date_freq.get(datetime) is None:
				date_freq[datetime] = [0,0]

			date_freq[datetime][0] += 1
			if '小並感' in post:
				date_freq[datetime][1] += 1
	except Exception as ex:
		print(ex)
		...
	#print(date_freq)
	return date_freq

args = [(index,path) for index, path in enumerate(list(Path('../posts').glob('*.jsonl')))]

date_freq = {}
with PPE(max_workers=12) as exe:
	for _date_freq in exe.map(pmap, args):
		for date, val in _date_freq.items():
			docs, freq = val
			if date_freq.get(date) is None:
				date_freq[date] = [0,0]
			date_freq[date][0] += docs
			date_freq[date][1] += freq
#print(date_freq)
for date, freq in sorted(date_freq.items()):
	if freq[0] <= 100:
		continue
	print(date, ' '.join([str(v) for v in freq]), freq[1]/freq[0] )
