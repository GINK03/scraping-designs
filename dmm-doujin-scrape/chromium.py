from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.action_chains import ActionChains

from selenium.webdriver.common.by import By


import bs4

import concurrent.futures

import hashlib

from pathlib import Path
import json
import gzip
import sys
import pickle
import time
import os
import random
from datetime import datetime

#url = 'https://www.pixiv.net/ranking.php?mode=daily&content=illust'

    
def getHTML(url):
  options = Options()
  options.add_argument('--headless')
  options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36")

  driver = webdriver.Chrome(chrome_options=options, executable_path='/usr/local/bin/chromedriver')
  driver.set_window_size(1024,1024*2)
  driver.get(url)
  html   = driver.page_source
  
  hashval = hashlib.sha256(bytes(url,'utf8')).hexdigest()
  driver.save_screenshot(f'ss/{hashval}.png')
  driver.quit() 
  return html
if __name__ == '__main__':
  getRanking()
