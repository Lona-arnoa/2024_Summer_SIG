# kiwi를 이용해서 명사 및 키워드를 추출하는 프로그램입니다.
import urllib.request
import urllib.parse
import requests
from bs4 import BeautifulSoup
import re
from konlpy.tag import Okt
from krwordrank.word import summarize_with_keywords
from kiwipiepy import Kiwi


# 초기 설정
okt = Okt()
kiwi = Kiwi()

client_id = "_C12LIJCwlme2ozPrU3k"  # 네이버 오픈 API ID
client_secret = "Gehzb9ohra"  # 네이버 오픈 API secret

# 검색어 입력 받기
quote = input("검색할 단어 : ")
encText = urllib.parse.quote(quote)
display_num = input("검색 갯수 입력 : ")

# 검색어 분리 저장
def split_string_to_array(string):
    words_array = string.split()
    return words_array

# 네이버 API를 통해 블로그 검색
url = f"https://openapi.naver.com/v1/search/blog?query={encText}&display={display_num}"
request = urllib.request.Request(url)
request.add_header("X-Naver-Client-Id", client_id)
request.add_header("X-Naver-Client-Secret", client_secret)
response = urllib.request.urlopen(request)
rescode = response.getcode()

if rescode == 200:
    response_body = response.read()
    print(response_body.decode('utf-8'))
else:
    print("Error Code:" + rescode)

body = response_body.decode('utf-8')
body = body.replace('"', '')
list1 = body.split('\n\t\t{\n\t\t\t')
list1 = [i for i in list1 if 'naver' in i]
print(list1)

links = []
for i in list1:
    title = re.findall('title:(.*?),\n\t\t\tlink', i)
    link = re.findall('link:(.*?),\n\t\t\tdescription', i)
    links.append(link)

links = [r for i in links for r in i]

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/100.0.48496.75"}
noneIframe_url = []

blog_links = []
for i in links:
    a = i.replace('\\', '')
    blog_links.append(a)

for i in blog_links:
    res = requests.get(i, headers=headers)
    html = BeautifulSoup(res.text, "html.parser")
    currency_url = 'https://blog.naver.com' + html.select_one('iframe')['src']
    noneIframe_url.append(currency_url)

contents = []

def preprocess_sentence_kr(w):
    w = w.strip()
    w = re.sub(r"[^0-9가-힣?.!,¿]+", " ", w)  # \n도 공백으로 대체
    w = w.strip()
    return w

# 명사만 추출하기
def noun_extractor(text):
    sentences = re.split(r'(?<=[.?!])\s+', text)  # 문장 단위로 분리
    noun_sentences = []

    for sentence in sentences:
        result = kiwi.analyze(sentence)
        nouns = [token for token, pos, _, _ in result[0][0] if (len(token) != 1 and pos.startswith('N')) or pos.startswith('SL')]
        noun_sentence = ' '.join(nouns)
        noun_sentences.append(noun_sentence)

    return noun_sentences

# 본문 추출 및 문장 단위로 쪼개기
for i in noneIframe_url:
    res = requests.get(i, headers=headers)
    html = BeautifulSoup(res.text, "html.parser")
    try:
        div = html.find('div', class_='se-main-container')
        if not div:
            continue
        content = preprocess_sentence_kr(div.text.replace('\n', ''))
        contents.append(content)
    except Exception as e:
        print(f"본문 {i} 추출 오류: {e}")
        continue

# 키워드 추출
for index, content in enumerate(contents):
    sentences = noun_extractor(content)
    print(f'본문 {index + 1} :\n{content}')
    print('--------------------------')
    print(f'명사 추출 {index + 1} :\n{sentences}')
    print('--------------------------')

    keywords = summarize_with_keywords(sentences)
    print("키워드 추출 결과:")
    for word, r in sorted(keywords.items(), key=lambda x: x[1], reverse=True)[:30]:
        # if r >= 0.5:
        print(f'{word:8s}:\t{r:.4f}')

    stopwords = split_string_to_array(quote)
    filtered_keywords = {word: score for word, score in keywords.items() if word not in stopwords}

    print("불용어 거른 키워드 추출 결과:")
    for word, r in sorted(filtered_keywords.items(), key=lambda x: x[1], reverse=True)[:30]:
        # if r >= 1.0:
        print(f'{word:8s}:\t{r:.4f}')
            
    print('--------------------------')

