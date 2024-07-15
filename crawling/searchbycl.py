from selenium import webdriver # 동적 사이트 수집
from webdriver_manager.chrome import ChromeDriverManager # 크롬 드라이버 설치
from selenium.webdriver.chrome.service import Service # 자동적 접근
from selenium.webdriver.chrome.options import Options # 크롭 드라이버 옵션 지정
from selenium.webdriver.common.by import By # find_element 함수 쉽게 쓰기 위함
from selenium.webdriver.common.keys import keys
import time # 필요 시 시간 지연 시키기 위해 사용

driver= webdriver.Chrome(service=Service(ChromeDriverManager().install()))



search = input("검색할 키워드 입력")

driver.get('http://www.naver.com')

time.sleep(3)

search_box = driver.find_element(By.CLASS_NAME, 'search_input_box')

search_box.send_keys(search)
search_box.send_keys(keys.ENTER)
time.sleep(1)