from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
import bs4
import hashlib
from pathlib import Path
import gzip
import sys
import pickle
import time
import os
import random
from concurrent.futures import ProcessPoolExecutor as PPE

def save_html_with_hash(html):
    Path(f'htmls').mkdir(exist_ok=True)
    compressed = gzip.compress(bytes(html, 'utf8'))
    ha = hashlib.sha256(compressed).hexdigest()
    with open(f'htmls/{ha}', 'wb') as fp:
        fp.write(compressed)

def run(arg):
    url, index = arg
    options = Options()
    options.add_argument('--headless')
    options.add_argument(
        "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36")
    driver = webdriver.Chrome(chrome_options=options,
                              executable_path='/usr/bin/chromedriver')

    ha = hashlib.sha256(bytes(url, 'utf8')).hexdigest()
    print(url)
    try:
        driver.get(url)
        html = driver.page_source
        soup = bs4.BeautifulSoup(html, 'lxml')
        belements =  soup.find_all('input', {'class':'LinkButton'})
        selements = driver.find_elements_by_xpath('//input[contains(@class,"LinkButton")]')
        #print(selements)
        element = selements[index]
        print('try', belements[index].get('value'))
        for i in range(10**10): 
            print('now', i+1, belements[index].get('value'))
            try:
                element.click()
                html = driver.page_source
                save_html_with_hash(html)
            except Exception as ex:
                print(ex)
            element = driver.find_element_by_xpath('//input[contains(@name,"fwListNaviBtnNext")]')
    except Exception as ex:
        print(ex)
    driver.quit()


url = 'https://www.hellowork.go.jp/servicef/130020.do?action=initDisp&screenId=130020'
args = []
for index in range(53):
    args.append((url, index))
with PPE(max_workers=53) as exe:
    exe.map(run, args)
