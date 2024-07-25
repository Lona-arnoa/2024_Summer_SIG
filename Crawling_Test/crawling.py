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



import requests
from bs4 import BeautifulSoup

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/100.0.48496.75"}
noneIframe_url = []

blog_links = []
for i in links:
    a = i.replace('\\','')
    blog_links.append(a)


for i in blog_links:
    res = requests.get(i, headers = headers)
    html = BeautifulSoup(res.text, "html.parser")
    currency_url = 'https://blog.naver.com'+html.select_one('iframe')['src']
    noneIframe_url.append(currency_url)


print(noneIframe_url)


contents = []

for i in noneIframe_url:
    res = requests.get(i, headers = headers)
    html = BeautifulSoup(res.text, "html.parser")

    a = html.find('div', 'se-main-container').text
    contents.append(a.replace('\n',''))

for i in contents:
    print('본문 : \n', i)
    print('--------------------------')

# 배열의 문장을 단어로 분리하는 함수
def split_sentences_into_words(sentences):
    words = []
    for sentence in sentences:
        words.extend(sentence.split())
    return words

# 파일에서 단어를 읽어오는 함수 (줄바꿈을 기준으로 하나씩 읽음)
def read_words_from_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        words = file.read().splitlines()
    return words

# 일치하는 단어를 새로운 파일에 저장하는 함수
from collections import Counter

def write_matching_words_to_file(array_words, file_words, output_filename):
    array_words_counter = Counter(array_words)
    file_words_counter = Counter(file_words)
    
    matching_words = set(array_words) & set(file_words)  # 중복을 제거한 공통 단어 집합
    
    # 각 단어의 빈도 합계를 저장할 딕셔너리
    word_frequencies = {word: array_words_counter[word] + file_words_counter[word] for word in matching_words}
    
    # 빈도수로 정렬 (빈도가 높은 순서대로)
    sorted_words = sorted(word_frequencies.items(), key=lambda item: item[1], reverse=True)
    
    with open(output_filename, 'w', encoding='utf-8') as output_file:
        for word, count in sorted_words:
            output_file.write(f"{word} {count}\n")

# 입력 파일과 출력 파일 이름
input_filename = r'C:\Users\aaron\OneDrive\Desktop\SIG\workspace\2024_Summer_SIG-main\crawling\input.txt'
output_filename = r'C:\Users\aaron\OneDrive\Desktop\SIG\workspace\2024_Summer_SIG-main\crawling\output.txt'

# 배열의 문장을 단어로 분리
array_words = split_sentences_into_words(contents)

# 파일에서 단어를 읽어옴
file_words = read_words_from_file(input_filename)

# 일치하는 단어를 출력 파일에 저장
write_matching_words_to_file(array_words, file_words, output_filename)