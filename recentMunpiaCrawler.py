from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime
from pytz import timezone
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import re
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


chrome_options = Options()

options = [
    "--headless",
    "--disable-gpu",
    "--window-size=1920,1200",
    "--ignore-certificate-errors",
    "--disable-extensions",
    "--no-sandbox",
    "--disable-dev-shm-usage"
]

for option in options:
    chrome_options.add_argument(option)

chrome_service = Service(ChromeDriverManager(version="113.0.5672.63").install())
driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

seoul_timezone = timezone('Asia/Seoul')
current_date = datetime.now(seoul_timezone).date()
formatted_date = current_date.strftime("%Y.%m.%d").strip()
date = current_date.strftime("%Y%m%d").strip()

list = []

url = []
title = []
author = []
description = []
image = []
genre = []

driver.get("https://square.munpia.com/boNewPlatinum")
driver.implicitly_wait(10)

while True:
    today = driver.find_element(By.CSS_SELECTOR,f'#ENTRIES > article:nth-child(1) > h3').text.replace('\n','.')
    i = 1
    found = True     
    while found:
      if today == formatted_date:
        article = driver.find_element(By.CSS_SELECTOR, f'#ENTRIES > article:nth-child({i})').get_attribute('class')
        if (i == 1):
          url = driver.find_element(By.CSS_SELECTOR, f'#ENTRIES > article:nth-child({i}) > a').get_attribute('href')                
          if url == 'https://novel.munpia.com/':
            i += 1
            continue
          driver.get(url)
          img = driver.find_element(By.CSS_SELECTOR, f'#board > div.novel-info.dl-horizontal.zoom > div.dt.cover-box > img').get_attribute('src')
          title = driver.find_element(By.CSS_SELECTOR,'#board > div.novel-info.dl-horizontal.zoom > div.dd.detail-box > h2 > div > a').get_attribute('title')
          title = re.sub(r"\s*\[.*?\]\s*", "", title)
          try:
            author = driver.find_element(By.CSS_SELECTOR,'#board > div.novel-info.dl-horizontal.zoom > div.dd.detail-box > dl.meta-author.meta > dd > a > strong').text
          except:
            author = driver.find_element(By.CSS_SELECTOR,'#board > div.novel-info.dl-horizontal.zoom > div.dd.detail-box > dl.meta-author.meta > dd').text
          genre = driver.find_element(By.CSS_SELECTOR,'#board > div.novel-info.dl-horizontal.zoom > div.dd.detail-box > p.meta-path > strong').text
          description = driver.find_element(By.CSS_SELECTOR, '#STORY-BOX > p.story').text.replace('\n',' ')
          description = description.lstrip('=')
          genre_array = [g.strip() for g in genre.split(",")]
          genre_list = ['BL', '공포·미스테리', '라이트노벨', '로맨스', '무협', '현대판타지', '판타지']
          genre_found = False
          for g in genre_list:
            if g in genre_array:
              genre = g
              genre_found = True
              break
            if not genre_found:
              genre = "판타지"

          if "로맨스" == genre:
            genre = "ROMANCE"
          elif "판타지" == genre:
            genre = "FANTASY"
          elif "현대판타지" == genre:
            genre = "MODERN_FANTASY"
          elif "무협" == genre:
            genre = "WUXIA"
          elif "공포·미스테리" == genre:
            genre = "MYSTERY"
          elif "라이트노벨" == genre:
            genre = "LIGHT_NOVEL"
          elif "BL" == genre:
            genre = "BL"
          lists = [title, author, description, genre, img, url]        
          list.append(lists)
          i += 1
          driver.back() 
        else:  
          if article == 'article gap':
            found = False
            break
          else:
            found = True
        url = driver.find_element(By.CSS_SELECTOR, f'#ENTRIES > article:nth-child({i}) > a').get_attribute('href')                
        if url == 'https://novel.munpia.com/':
          i += 1
          continue
        driver.get(url)
        img = driver.find_element(By.CSS_SELECTOR, f'#board > div.novel-info.dl-horizontal.zoom > div.dt.cover-box > img').get_attribute('src')
        title = driver.find_element(By.CSS_SELECTOR,'#board > div.novel-info.dl-horizontal.zoom > div.dd.detail-box > h2 > div > a').get_attribute('title')
        title = re.sub(r"\s*\[.*?\]\s*", "", title)
        try:
          author = driver.find_element(By.CSS_SELECTOR,'#board > div.novel-info.dl-horizontal.zoom > div.dd.detail-box > dl.meta-author.meta > dd > a > strong').text
        except:
          author = driver.find_element(By.CSS_SELECTOR,'#board > div.novel-info.dl-horizontal.zoom > div.dd.detail-box > dl.meta-author.meta > dd').text
        genre = driver.find_element(By.CSS_SELECTOR,'#board > div.novel-info.dl-horizontal.zoom > div.dd.detail-box > p.meta-path > strong').text
        description = driver.find_element(By.CSS_SELECTOR, '#STORY-BOX > p.story').text.replace('\n',' ')
        description = description.lstrip('=')
        genre_array = [g.strip() for g in genre.split(",")]
        genre_list = ['BL', '공포·미스테리', '라이트노벨', '로맨스', '무협', '현대판타지', '판타지']
        genre_found = False
        for g in genre_list:
          if g in genre_array:
            genre = g
            genre_found = True
            break
          if not genre_found:
            genre = "판타지"

        if "로맨스" == genre:
          genre = "ROMANCE"
        elif "판타지" == genre:
          genre = "FANTASY"
        elif "현대판타지" == genre:
          genre = "MODERN_FANTASY"
        elif "무협" == genre:
          genre = "WUXIA"
        elif "공포·미스테리" == genre:
          genre = "MYSTERY"
        elif "라이트노벨" == genre:
          genre = "LIGHT_NOVEL"
        elif "BL" == genre:
          genre = "BL"
        lists = [title, author, description, genre, img, url]        
        list.append(lists)
        i += 1
        driver.back()       
      else:
        break
    break


        
df = pd.DataFrame(list, columns = ('제목', '작가', '소개', '장르', '이미지', '링크'))

df.to_csv(date+'munpia.csv', encoding = 'utf-8-sig', mode = 'w', index = False)
