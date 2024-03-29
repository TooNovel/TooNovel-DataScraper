from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime
from pytz import timezone
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

formatted_date = current_date.strftime("%Y.%m.%d.").strip()
date = current_date.strftime("%Y%m%d").strip()

list = []

url = []
title = []
author = []
description = []
image = []
genre = []

driver.get("https://series.naver.com/novel/recentList.series")
driver.implicitly_wait(10)

found_match = False

while True:
  found_match = False
  for i in range(1,26):
    try:
      today = driver.find_element(By.CSS_SELECTOR,f'#content > div > ul > li:nth-child({i}) > div > p.info').text
      split_parts = today.split("|")
      date_part = split_parts[2].strip()
    except:
      found_match = False
      break
    if date_part == formatted_date:
      found_match = True
      url = driver.find_element(By.CSS_SELECTOR, f'#content > div > ul > li:nth-child({i}) > a').get_attribute('href')
      img = driver.find_element(By.CSS_SELECTOR, f'#content > div > ul > li:nth-child({i}) > a > img').get_attribute('src')
      if(img == 'https://ssl.pstatic.net/static/nstore/thumb/19over_book2_79x119.gif'):
        continue
      else:
        driver.get(url)
        title = driver.find_element(By.CSS_SELECTOR,'#content > div.end_head > h2').text
        title = re.sub(r"\s*\[.*?\]\s*", "", title)
        author = driver.find_element(By.CSS_SELECTOR,'#content > ul.end_info.NE\=a\:nvi > li > ul > li:nth-child(3) > a').text
        genre = driver.find_element(By.CSS_SELECTOR,'#content > ul.end_info.NE\=a\:nvi > li > ul > li:nth-child(2) > span > a').text
        try:
          img = driver.find_element(By.CSS_SELECTOR, '#container > div.aside.NE\=a\:nvi > span > img').get_attribute('src')
        except:
          img = driver.find_element(By.CSS_SELECTOR, '#container > div.aside.NE\=a\:nvi > a > img').get_attribute('src')
        try:
          driver.find_element(By.CSS_SELECTOR,'#content > div.end_dsc > div:nth-child(1) > span > a').click()
          description = driver.find_element(By.CSS_SELECTOR, '#content > div.end_dsc.open > div:nth-child(2)').text.replace('\n',' ').replace('접기','')
          description = description.lstrip('=')
        except:
          description = driver.find_element(By.CSS_SELECTOR,'#content > div.end_dsc > div').text.replace('\n',' ')
          description = description.lstrip('=')

        if "로판" in genre:
            genre = "ROMANCE_FANTASY"
        elif "로맨스" in genre:
            genre = "ROMANCE"
        elif "판타지" in genre:
            genre = "FANTASY"
        elif "현판" in genre:
            genre = "MODERN_FANTASY"
        elif "무협" in genre:
            genre = "WUXIA"
        elif "미스터리" in genre:
            genre = "MYSTERY"
        elif "라이트노벨" in genre:
            genre = "LIGHT_NOVEL"
        elif "BL" in genre:
            genre = "BL"

        lists = [title, author, description, genre, img, url]        
        list.append(lists)
        driver.back()
    else:
      continue
  if not found_match:
    break
  driver.find_element(By.CSS_SELECTOR, '#content > p > span.next > a').click()


        
df = pd.DataFrame(list, columns = ('제목', '작가', '소개', '장르', '이미지', '링크'))

df.to_csv(date+'series.csv', encoding = 'utf-8-sig', mode = 'w', index = False)