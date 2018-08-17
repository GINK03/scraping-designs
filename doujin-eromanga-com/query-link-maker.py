import glob
import re
import json
import click

h2_hash   = {}
tag_hashs = {}
hash_imgs = {}

for fn in glob.glob('./static_folder/*/*'):
  if re.search(r'\.json$', fn) is None:
    continue
  print(fn)
  obj = json.load(open(fn))
  print(obj)
  h2   = obj['h2']
  tags = obj['tags']
  hashval = re.search(r'/static_folder/(.*?)/obj.json', fn).group(1)
  print(hashval)
  h2_hash[h2] = hashval
  for tag in tags:
    if tag_hashs.get(tag) is None:
      tag_hashs[tag] = []
    tag_hashs[tag].append( hashval )
  for img_fn in glob.glob(f'./static_folder/{hashval}/*.jpg'):
    #戦闘の.を削除
    img_fn = img_fn[1:] 
    #print(img_fn)
    if hash_imgs.get(hashval) is None:
      hash_imgs[hashval] = []
    hash_imgs[hashval].append(img_fn)

@click.command()
@click.option('--mode', default='make_query', help='make_query')
def main(mode):
  if mode == 'make_query':
    json.dump(h2_hash,  fp=open('h2_hash.json', 'w')  , indent=2, ensure_ascii=False)
    json.dump(tag_hashs,fp=open('tag_hashs.json', 'w'), indent=2, ensure_ascii=False)
    json.dump(hash_imgs,fp=open('hash_imgs.json', 'w'), indent=2, ensure_ascii=False)

if __name__ == '__main__':
  main()
