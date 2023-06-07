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


chrome_service = Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())

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

driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

seoul_timezone = timezone('Asia/Seoul')
current_date = datetime.now(seoul_timezone).date()
print(current_date)
formatted_date = current_date.strftime("%Y.%m.%d").strip()
date = current_date.strftime("%Y%m%d").strip()

list = []

url = []
title = []
author = []
description = []
image = []
genre = []

driver.get("https://page.kakao.com/menu/10000/screen/50?category_uid=11")
driver.implicitly_wait(10)

while True:
  count = driver.find_element(By.CSS_SELECTOR, '#__next > div > div.flex.w-full.grow.flex-col.px-122pxr > div > div.flex.grow.flex-col > div.mb-4pxr.flex-col > div > div:nth-child(3) > div.mb-4pxr.flex.h-44pxr.w-full.justify-between.px-4pxr.pt-15pxr.pb-7pxr > span.font-small2.text-el-40.css-1797ph-Text').text
  count = int(re.findall(r'\d+', count)[0])
  print(count)
  for i in range(1,count+1):
    today = driver.find_element(By.CSS_SELECTOR,f'#__next > div > div.flex.w-full.grow.flex-col.px-122pxr > div > div.flex.grow.flex-col > div.mb-4pxr.flex-col > div > div:nth-child(3) > div.mb-4pxr.flex.h-44pxr.w-full.justify-between.px-4pxr.pt-15pxr.pb-7pxr > span.font-medium1-bold.text-el-60.css-1797ph-Text').text
    print(today)
    if today == 'TODAY':
      print(123)
      try:
        url = driver.find_element(By.CSS_SELECTOR, f'#__next > div > div.flex.w-full.grow.flex-col.px-122pxr > div > div.flex.grow.flex-col > div.mb-4pxr.flex-col > div > div:nth-child(3) > div.w-full.overflow-hidden > div > div:nth-child({i}) > div > a').get_attribute('href')
        print(url)
      except:
        url = driver.find_element(By.CSS_SELECTOR, f'#__next > div > div.flex.w-full.grow.flex-col.px-122pxr > div > div.flex.grow.flex-col > div.mb-4pxr.flex-col > div > div:nth-child(3) > div.w-full.overflow-hidden > div > div > div > a').get_attribute('href')
        print(url)
      try:
        img = driver.find_element(By.CSS_SELECTOR, f'#__next > div > div.flex.w-full.grow.flex-col.px-122pxr > div > div.flex.grow.flex-col > div.mb-4pxr.flex-col > div > div:nth-child(3) > div.w-full.overflow-hidden > div > div:nth-child({i}) > div > a > div > div.relative.rounded-8pxr.overflow-hidden.w-full.h-full.css-1dbppub-Image > img').get_attribute('src')
        print(img)
      except:
        img = driver.find_element(By.CSS_SELECTOR, f'#__next > div > div.flex.w-full.grow.flex-col.px-122pxr > div > div.flex.grow.flex-col > div.mb-4pxr.flex-col > div > div:nth-child(3) > div.w-full.overflow-hidden > div > div > div > a > div > div.relative.rounded-8pxr.overflow-hidden.w-full.h-full.css-1dbppub-Image > img').get_attribute('src')
        print(img)
      driver.get(url)
      try:
        title = driver.find_element(By.CSS_SELECTOR,'#__next > div > div.flex.w-full.grow.flex-col.px-122pxr > div.flex.h-full.flex-1 > div.mb-28pxr.flex.w-320pxr.flex-col > div:nth-child(1) > div.w-320pxr.css-0 > div > div.css-0 > div.relative.text-center.mx-32pxr.py-24pxr > span').text
        title = re.sub(r"\s*\[.*?\]\s*", "", title)
        print("제목 : "+title)
        author = driver.find_element(By.CSS_SELECTOR,'#__next > div > div.flex.w-full.grow.flex-col.px-122pxr > div.flex.h-full.flex-1 > div.mb-28pxr.flex.w-320pxr.flex-col > div:nth-child(1) > div.w-320pxr.css-0 > div > div.css-0 > div.relative.text-center.mx-32pxr.py-24pxr > div:nth-child(2) > div.flex.items-center.justify-center.mt-4pxr.flex-col.text-el-50.opacity-100.all-child\:font-small2 > div.mt-4pxr > span').text
        print("작가 : "+author)
        genre = driver.find_element(By.CSS_SELECTOR,'#__next > div > div.flex.w-full.grow.flex-col.px-122pxr > div.flex.h-full.flex-1 > div.mb-28pxr.flex.w-320pxr.flex-col > div:nth-child(1) > div.w-320pxr.css-0 > div > div.css-0 > div.relative.text-center.mx-32pxr.py-24pxr > div:nth-child(2) > div.flex.items-center.justify-center.mt-16pxr.text-el-60.all-child\:font-small2 > span:nth-child(9)').text
        print("장르 : "+genre)
        driver.find_element(By.CSS_SELECTOR,'#__next > div > div.flex.w-full.grow.flex-col.px-122pxr > div.flex.h-full.flex-1 > div.mb-28pxr.ml-4px.flex.w-632pxr.flex-col > div.relative.flex.w-full.flex-col.my-0.bg-bg-a-20.px-15pxr.pt-28pxr.pb-12pxr > div > div > div:nth-child(2) > a').click()
        description = driver.find_element(By.CSS_SELECTOR, '#__next > div > div.flex.w-full.grow.flex-col.px-122pxr > div.flex.h-full.flex-1 > div.mb-28pxr.ml-4px.flex.w-632pxr.flex-col > div.flex-1.bg-bg-a-20 > div.text-el-60.break-keep.py-20pxr.pt-31pxr.pb-32pxr > span').text.replace('\n',' ')
        description = description.lstrip('=')
        print("소개 : " + description)

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
        elif "BL" in genre:
            genre = "BL"
        elif "드라마" in genre:
            genre = "MODERN_FANTASY"

        lists = [title, author, description, genre, img, url]        
        list.append(lists)
        driver.back()
        driver.back()
      except:
        text = driver.find_element(By.CSS_SELECTOR, '#__next > div > div.flex.w-full.grow.flex-col.px-122pxr > div > div > div > div.mt-8pxr > div').text.replace('\n', '')
        print(text)
        if text == '서비스 이용을 위해 연령 확인이 필요 합니다.로그인 후 이용해 주세요.':
          driver.back()
          continue
    else:
      continue
  else:
    break


        
df = pd.DataFrame(list, columns = ('제목', '작가', '소개', '장르', '이미지', '링크'))
print(df.head(6))

df.to_csv(date+'page.csv', encoding = 'utf-8-sig', mode = 'w', index = False)