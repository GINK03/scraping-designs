import requests
import os
import schedule
import time
import json
def job():
  os.system('python3 10-xml_parse.py')
  os.system('python3 20-darturl-clean.py')

schedule.every(10).minutes.do(job)
job()
while True:
  schedule.run_pending()
  time.sleep(1)
