from bs4 import BeautifulSoup
from pathlib import Path
import glob
import gzip
import re

def fee_parsing(fee):
    mm = re.search(r'((\d|,|万|千|\.){1,}円)', fee)
    if mm is None:
        return 
    mt = re.search(r'(((日|時|年|月)給|年収))', fee)
    money = mm.group(1).replace(',', '')
    if re.search('\d{1,}万\d{1,}円', money) is not None:
        money = money.replace('万', '')
    else:
        money = money.replace('万', '0000')
    money = int(money.replace('円', ''))
    if mt.group(1) in {'時給'}:
        money *= 8*20
    if mt.group(1) in {'日給'}:
        money *= 20
    if mt.group(1) in {'年収'}:
        money //= 12
    #print(mt.group(1), money)
    #print(mt, mm)
    return money

def area_parsing(area):
    area = sorted(area.split('\n'), key=lambda x:len(x))
    return area[-1]
for fn in glob.glob('./htmls/*'):
    try:
        html = (gzip.decompress(open(fn, 'rb').read()).decode())
    except Exception as ex:
        print(ex)
        continue
    soup = BeautifulSoup(html)

    ogurl = soup.find('meta', {'property':'og:url'})
    if ogurl is None:
        continue
    ogurl = (ogurl.get('content'))
    if '/jb/' not in ogurl:
        continue
    print(ogurl)
    table = soup.find('div', {'class':'p-detail-table'})
    if table is None:
        continue

    obj = {}
    for dl in table.find_all('dl'):
        #print(dl)
        dt = dl.find('dt').find('span')
        class_last = dt.get('class')[-1]
        dd = dl.find('dd')
        #print(class_last, dd.text.strip())
        obj[class_last] = dd.text.strip()
    try:
        money = fee_parsing(obj['p-detail-table_icon_fee'])
    except Exception as ex:
        print(ex)
        continue
    try:
        area = area_parsing(obj['p-detail-table_icon_area'])
    except Exception as ex:
        print(ex)
        continue
    
    print(obj)
    print(area, money) 
