# krwordrank를 이용해서 키워드를 추출하는 프로그램입니다.
import urllib.request
from konlpy.tag import Okt
import requests
from bs4 import BeautifulSoup
from konlpy.tag import Okt
from krwordrank.word import summarize_with_keywords
import re

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

links = []
for i in list1:
    title = re.findall('title:(.*?),\n\t\t\tlink',i)
    link = re.findall('link:(.*?),\n\t\t\tdescription',i)
    links.append(link)

links = [r for i in links for r in i]

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

def split_noun_sentences(text):
    okt = Okt()
    sentences = text.replace(". ",".")
    sentences = re.sub(r'([^\n\s\.\?!]+[^\n\.\?!]*[\.\?!])', r'\1\n', sentences).strip().split("\n")
    # return sentences
    result = []
    for sentence in sentences:
        if len(sentence) == 0:
            continue
        sentence_pos = okt.pos(sentence, stem=True)
        nouns = [word for word, pos in sentence_pos if pos == 'Noun']
        if len(nouns) == 1:
            continue
        result.append(' '.join(nouns) + '.')
        
    return result

for i in contents:
    sentence_list2 = split_noun_sentences(i)
    print(sentence_list2)
    print('--------------------------------------------------------------------------------------')
    keywords = summarize_with_keywords(sentence_list2)
    print(keywords)
    print('--------------------------------------------------------------------------------------')