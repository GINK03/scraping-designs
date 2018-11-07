from pathlib import Path
import json
from concurrent.futures import ProcessPoolExecutor as PPE



def pmap(arg):
	key,paths = arg
	date_freq = {}
	for path in paths:
		try:
			obj = json.load(path.open())
		except:
			continue
		datetime = obj['datetime']
		if date_freq.get(datetime) is None:
			date_freq[datetime] = 0
		date_freq[datetime] += 1
	return date_freq

key_paths = {}
for index, path in enumerate(Path('../posts').glob('*.json')):
	key = index%12
	if key_paths.get(key) is None:
		key_paths[key] = []
	key_paths[key].append(path)
args = [(key,paths) for key,paths in key_paths.items()]

date_freq = {}
with PPE(max_workers=12) as exe:
	for _date_freq in exe.map(pmap, args):
		for date, freq in _date_freq.items():
			if date_freq.get(date) is None:
				date_freq[date] = 0
			date_freq[date] += freq
	
for date, freq in sorted(date_freq.items()):
	print(date, freq)
