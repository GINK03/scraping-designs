from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

import bs4

import concurrent.futures

import hashlib

from pathlib import Path

import gzip
import sys
import pickle
import time
import os
import random
URL = 'http://mangamura.org'

#def _right_click(driver):
def _map(arg):
  url = arg
  options = Options()
  options.add_argument('--headless')
  options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36")

  driver = webdriver.Chrome(chrome_options=options,executable_path='/usr/bin/chromedriver')

  return_chunk = dict()
  
  ha = hashlib.sha256(bytes(url, 'utf8')).hexdigest()
  print(url)
  try:
    driver.get(url)
    time.sleep(2.0)
    
    for i in range(200):
      if i == 0:
        action = webdriver.common.action_chains.ActionChains(driver)
        el=driver.find_elements_by_xpath("//body")[0]
        action.move_to_element_with_offset(el, 5, 100)
        action.click()
        action.perform()
        time.sleep(3.)
      html = driver.page_source
      soup = bs4.BeautifulSoup(html, 'lxml')
      for img in soup.findAll('img'):
        #print(img) 
        if img.get('id') is not None and img.get('src') != '':
          try:
            os.mkdir(f'imgs/{ha}')
          except:
            ...
          id = img.get('id')
          src = img.get('src')
          open(f'imgs/{ha}/{id}', 'w').write( src )
     
      try:
        os.mkdir(f'sss/{ha}')
      except:
        ...
      # もしキャプチャがあれば、キャプチャをクリックする
      try:
        time.sleep( random.randint(3, 10)/10.0 )
        iframe = driver.find_element_by_tag_name("iframe")
        driver.switch_to_frame(iframe)
        num = driver.find_element_by_id('recaptcha-anchor')
        #if num != []:
        time.sleep( random.randint(3, 10)/10.0 )
        driver.find_element_by_id('recaptcha-anchor')[0].click()
        time.sleep(5.0)
        print(f'handle captcha')
      except Exception as ex:
        print(f'No recaptcha! {ex}')
        ...
      driver.switch_to_default_content()

      driver.save_screenshot(f'sss/{ha}/{ha}_{i}.png')
      action = webdriver.common.action_chains.ActionChains(driver)
      el=driver.find_elements_by_xpath("//body")[0]
      action.move_to_element_with_offset(el, 5, 100)
      action.click()
      action.perform()
      time.sleep(2.)
  except Exception as ex:
    print(ex)
  driver.quit() 
  return return_chunk

urls = ['http://mangamura.org/kai_pc_viewer?p=1499591881']
#_map(urls[0])

urls = pickle.loads(gzip.decompress(open('pc_viewer_urls.pkl.gz', 'rb').read()))

with concurrent.futures.ProcessPoolExecutor(max_workers=32) as exe:
  exe.map(_map, urls)

