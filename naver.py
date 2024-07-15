import os
import sys
import urllib.request

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

blog_links = []
for i in links:
    a = i.replace('\\','')
    b = a.replace('?Redirect=Log&logNo=','/')

print(blog_links)
print('생성된 링크 갯수 ; ', len(blog_links),'개')