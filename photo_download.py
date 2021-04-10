import requests 
import shutil   
import re
import time
import os

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from lxml import html

URL = 'https://unsplash.com/@davidkovalenkoo'
save_path = '@' + URL.split('@')[1]

def make_dir ():
    if not os.path.exists(save_path):
        os.makedirs(save_path)

def get_page(url):
    driver = webdriver.Chrome(service_log_path=os.devnull)
    driver.maximize_window()        
    driver.get(url)
    button = driver.find_element_by_class_name('_1hjZT._1nvjo._3jtP1._3d86A._1CBrG._2aM5L.Onk5k._19rc8.hhSId')
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')    
    time.sleep(.5)
    button.click()
    time.sleep(.5)
    driver.execute_script('window.scrollTo(0, 0);')
    num_photos = driver.find_element_by_class_name('_3ruL8.xLon9')
    for i in range(int(num_photos.text)):
        driver.execute_script('window.scrollBy(0, 125);')    
        time.sleep(.4)
    height = driver.execute_script("return document.body.scrollHeight")
    print(height)
    html = driver.page_source
    driver.close()
    return html

def get_links(url):
    result = {} # 'title':'link'

    soup = BeautifulSoup(get_page(url), 'html.parser')
    
    column_div = soup.findAll('div', {'class':'qztBA','style':'--column-gutter:24px;--columns:3','data-test':'masonry-grid-count-three'})
    columns = column_div[0].findAll('div',{'class':'_1ZjfQ'})
    
    photos_in_column = []
    for i in range(len(columns)):
        photos_in_column.append(columns[i].findAll('a',{'itemprop':'contentUrl'}))

    count = 0
    for i in range(len(photos_in_column)):
        for link in photos_in_column[i]:
            count += 1
            result[link['title']] = link['href']

    print('num photos:' + str(len(result)))
    return result

def download_photo (url, filename):
    image_url = url

    r = requests.get(image_url, stream = True)

    if r.status_code == 200:
        r.raw.decode_content = True

        with open(save_path + filename,'wb') as f:
            shutil.copyfileobj(r.raw, f)

        print('Image sucessfully Downloaded: ', filename)
    else:
        print('Image Couldn\'t be retreived')

def main (url):
    make_dir()
    result = get_links(URL)

    for title,link in result.items():
        url = 'https://unsplash.com' + str(link) + '/download?force=true'
        filename = str(title) + '.jpeg'
        print(url + '  ' + filename)
        download_photo(url,filename)
        time.sleep(.5)

# get_page(URL)
# get_links(URL)
main(URL)