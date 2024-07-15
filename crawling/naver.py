import os
import sys
import urllib.request

from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

client_id = "_C12LIJCwlme2ozPrU3k" #네이버 오픈 API ID
client_secret = "Gehzb9ohra" #네이버 오픈 API secret

quote = input("검색할 단어 : ")
encText = urllib.parse.quote(quote)

display_num = input("검색 갯수 입력 : ")

url = "https://openapi.naver.com/v1/search/blog?query=" + encText + "&display=" + display_num # JSON 결과 URL
# url = "https://openapi.naver.com/v1/search/blog.xml?query=" + encText # XML 결과

request = urllib.request.Request(url)
request.add_header("X-Naver-Client-Id",client_id)
request.add_header("X-Naver-Client-Secret",client_secret)
response = urllib.request.urlopen(request)
rescode = response.getcode()

if(rescode==200):
    response_body = response.read()
    print(response_body.decode('utf-8'))
else:
    print("Error Code:" + rescode)

body = response_body.decode('utf-8')
body = body.replace('"','')
list1 = body.split('\n\t\t{\n\t\t\t')
list1 = [i for i in list1 if 'naver' in i]
print(list1)

import re
titles = []
links = []
for i in list1:
    title = re.findall('title:(.*?),\n\t\t\tlink',i)
    link = re.findall('link:(.*?),\n\t\t\tdescription',i)
    titles.append(title)
    links.append(link)

titles = [r for i in titles for r in i]
links = [r for i in links for r in i]

print('<<제목 모음>>')
print(titles)
print('총 제목 수: ',len(titles),'개')
print('\n<<링크 모음>>')
print(links)
print('총 링크 수: ',len(links),'개')

import time
from selenium import webdriver # 동적 사이트 수집
from webdriver_manager.chrome import ChromeDriverManager # 크롬 드라이버 설치
from selenium.webdriver.chrome.service import Service # 자동적 접근
from selenium.webdriver.chrome.options import Options # 크롭 드라이버 옵션 지정
from selenium.webdriver.common.by import By # find_element 함수 쉽게 쓰기 위함
from selenium.webdriver.common.keys import keys

driver= webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.implicitly_wait(3)

contents = []
for i in links:
    #블로그 링크 하나씩 불러오기
    driver.get(i)
    time.sleep(1)
    #블로그 안 본문이 있는 iframe에 접근하기
    driver.switch_to.frame("mainFrame")
    #본문 내용 크롤링하기
    try:
        a = driver.find_element(By.CSS_SELECTOR,'div.se-main-container').text
        contents.append(a)
    # NoSuchElement 오류시 예외처리(구버전 블로그에 적용)
    except NoSuchElementException:
        a = driver.find_element(By.CSS_SELECTOR,'div#content-area').text
        contents.append(a)

    print('본문: \n', a)

driver.quit()
print("<<본문 크롤링 완료.>>")