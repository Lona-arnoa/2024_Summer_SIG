import os
import sys
import urllib.request
from konlpy.tag import Okt
from collections import Counter

okt=Okt()

client_id = "_C12LIJCwlme2ozPrU3k" #네이버 오픈 API ID
client_secret = "Gehzb9ohra" #네이버 오픈 API secret

quote = input("검색할 단어 : ")
encText = urllib.parse.quote(quote)

display_num = input("검색 갯수 입력 : ")

url = "https://openapi.naver.com/v1/search/blog?query=" + encText + "&display=" + display_num # JSON 결과 URL

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
links = []
for i in list1:
    title = re.findall('title:(.*?),\n\t\t\tlink',i)
    link = re.findall('link:(.*?),\n\t\t\tdescription',i)
    links.append(link)

links = [r for i in links for r in i]

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

def preprocess_sentence_kr(w):
    w = w.strip()
    w = re.sub(r"[^0-9가-힣?.!,¿]+", " ", w) # \n도 공백으로 대체해줌
    w = w.strip()
    return w

for i in noneIframe_url:
    res = requests.get(i, headers = headers)
    html = BeautifulSoup(res.text, "html.parser")
    try:
        a = html.find('div', 'se-main-container').text
        contents.append(preprocess_sentence_kr(a.replace('\n','')))
    except Exception as e:
        continue

for i in contents:
    print('본문 : \n', i)
    print('--------------------------')

# 문자열 배열에 okt.morphs 적용
contents_noun = [okt.morphs(text) for text in contents]

# 평탄화
flattened_contents_noun = [noun for sublist in contents_noun for noun in sublist]

print(flattened_contents_noun)

# 파일에서 단어를 읽어오는 함수 (줄바꿈을 기준으로 하나씩 읽음)
def read_words_from_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        words = file.read().splitlines()
    return words

# 일치하는 단어를 빈도수에 따라 정렬하여 새로운 파일에 저장하는 함수
def write_matching_words_to_file(contents_noun, file_words, output_filename):
    contents_noun_counter = Counter(contents_noun)
    file_words_counter = Counter(file_words)
    
    matching_words = set(contents_noun) & set(file_words)  # 중복을 제거한 공통 단어 집합
    
    # 각 단어의 빈도 합계를 저장할 딕셔너리
    word_frequencies = {word: contents_noun_counter[word] + file_words_counter[word] for word in matching_words}
    
    # 빈도수로 정렬 (빈도가 높은 순서대로)
    sorted_words = sorted(word_frequencies.keys(), key=lambda word: word_frequencies[word], reverse=True)
    
    with open(output_filename, 'w', encoding='utf-8') as output_file:
        for word in sorted_words:
            output_file.write(f"{word} {word_frequencies[word]}\n")

# 입력 파일과 출력 파일 이름
input_filename = r'C:\Users\Lona\OneDrive\Desktop\SIG\workspace\2024_Summer_SIG-main\Crawling\CategoryList.txt'
output_filename = r'C:\Users\Lona\OneDrive\Desktop\SIG\workspace\2024_Summer_SIG-main\Crawling\ResultList.txt'

# 파일에서 단어를 읽어옴
file_words = read_words_from_file(input_filename)

# 일치하는 단어를 출력 파일에 저장
write_matching_words_to_file(flattened_contents_noun, file_words, output_filename)