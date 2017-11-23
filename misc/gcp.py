import json
import os
import re

data = os.popen('gcloud compute instances list --format json').read()
print(data)

name_ip = {}
for data in json.loads( data ):
  if data['scheduling']['preemptible'] != True:
    continue
  if data['status'] != 'RUNNING':
    continue
  try:
    name = data['name']
    print(  data['networkInterfaces'][0] )
    ip = data['networkInterfaces'][0]['accessConfigs'][0]['natIP']
  except KeyError as e:
    continue
  print(name, ip )
  name_ip[name] = ip

open('name_ip.json', 'w').write( json.dumps(name_ip,indent=2) )
