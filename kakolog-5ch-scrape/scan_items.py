import os
import glob
import gzip
import bs4, lxml
import concurrent.futures
import re
import hashlib
import json
from pathlib import Path
def _map(arg):
	index, names = arg
	for name in names:
		print(name)
		html = gzip.decompress(open(name, 'rb').read()).decode()
		soup = bs4.BeautifulSoup(html, 'html5lib')
		for script in soup(["script", "style"]):
			script.extract()		# rip it out
		#for d in soup.find_all('div'):
		#		print(d)
		if soup.find('dl', {'class':'thread'}) is None:
			continue
		dts = soup.find('dl', {'class':'thread'}).find_all('dt')
		dds = soup.find('dl', {'class':'thread'}).find_all('dd')
		for dt,dd in zip(dts,dds):
			try:
				user = dt.find('b').text
				datetime = re.search(r'\d\d\/\d\d/\d\d', dt.text).group(0)
				post = re.sub(r'\n', ' ', dd.text)
				obj = {'user':user, 'datetime':datetime, 'post':post}
				ser = json.dumps(obj, indent=2, ensure_ascii=False)
				hashed = hashlib.sha256(bytes(ser, 'utf8')).hexdigest()
				Path(f'posts/{datetime}').mkdir(parents=True, exist_ok=True)
				if Path(f'posts/{datetime}/{hashed}.json').exists():
					continue
				open(f'posts/{datetime}/{hashed}.json', 'w').write( ser )
				#print(user, datetime, post)
			except Exception as ex:
				print(ex)
				print(dt.text)
args = {}
for index,name in enumerate(glob.glob('htmls/*')):
	key = index%12
	if args.get(key) is None:
		args[key] = []
	args[key].append(name)
args = [(key, names) for key,names in args.items()]
#[_map(arg) for arg in args]
with concurrent.futures.ProcessPoolExecutor(max_workers=12) as exe:
	exe.map( _map, args)
