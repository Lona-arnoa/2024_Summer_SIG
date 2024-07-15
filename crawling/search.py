from bs4 import BeautifulSoup
import requests


search = input("검색할 키워드 입력")

page = int(input("크롤링 할 페이지 수 입력"))

print("크롤링할 페이지 :",page,"페이지")

page_num = 0

if page == 1:
    page_num = 1
elif page == 0:
    page_num = 1
else:
    page_num = page+9*(page-1)

searchurl = "https://search.naver.com/search.naver?nso=&page=2&query="+ search + "&sm=tab_pge&start="+str(page_num)+"&where=web"
print("생성 url : ", searchurl)



headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/100.0.48496.75"}
original_html = requests.get(searchurl, headers = headers)
html = BeautifulSoup(original_html.text, "html.parser")

links = html.find_all(class_ = "total_tit")
url=[]
url.append(links[13].find("a")["href"])

search_html = requests.get(url[0], headers = headers)
get = BeautifulSoup(search_html.text, "html.parser")

mainText = get.get_text()
print(mainText)

print(get.find_all("p"))




