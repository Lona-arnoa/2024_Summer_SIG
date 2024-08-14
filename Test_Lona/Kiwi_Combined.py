# kiwi(Korean Intelligent Word Identifier) 통합코드입니다.
import urllib.request
import urllib.parse
import requests
from bs4 import BeautifulSoup
import re
import json
import time
from krwordrank.word import summarize_with_keywords
from collections import Counter
from kiwipiepy import Kiwi

# 초기 설정
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

# 키워드 추출 및 카테고리 가져오기
output_filename = r'C:\Users\Lona\OneDrive\Desktop\SIG\workspace\2024_Summer_SIG-main\Test_Lona\KiwiList.txt'

def fetch_category_from_api(keywords):
    encText = urllib.parse.quote(keywords)
    url = "https://openapi.naver.com/v1/search/shop?query=" + encText + "&display=1&start=1"  # JSON 결과
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", client_id)
    request.add_header("X-Naver-Client-Secret", client_secret)
    
    retries = 5
    for i in range(retries):
        try:
            with urllib.request.urlopen(request) as response:
                if response.getcode() == 200:
                    response_json = json.loads(response.read().decode('utf-8'))
                    items = response_json.get('items', [])
                    if items:
                        first_item = items[0]
                        category4 = first_item.get('category4', '').strip()
                        category3 = first_item.get('category3', '').strip()
                        category2 = first_item.get('category2', '').strip()

                        category = category4 or category3 or category2 or 'No category'
                        category = category.replace('기타', '').replace('여성', '').replace('남성', '').strip()
                        return category
                    return 'NO items'
                return f"Error Code: {response.getcode()}"
        except urllib.error.HTTPError as e:
            if e.code == 429:
                wait_time = 2 ** i
                print(f"요청이 너무 많습니다. {wait_time}초 후에 다시 시도합니다...")
                time.sleep(wait_time)
            else:
                return f"데이터 가져오기 오류: {e}"
        except Exception as e:
            return f"Error fetching data: {e}"

def write_categories_to_file(categories, output_filename):
    filtered_categories = [category for category in categories if category != 'NO items']
    category_counter = Counter(filtered_categories)
    sorted_categories = sorted(category_counter.items(), key=lambda item: item[1], reverse=True)
    
    with open(output_filename, 'w', encoding='utf-8') as output_file:
        for category, count in sorted_categories:
            category = category.replace('기타', '').replace('여성', '').replace('남성', '').strip()  # '기타' 제거
            output_file.write(f"{category} {count}\n")

def main():
    categories = []
    for index, content in enumerate(contents):
        sentences = noun_extractor(content)
        print(f'본문 {index + 1} :\n{content}')
        print('--------------------------')
        print(f'명사 추출 {index + 1} :\n{sentences}')
        print('--------------------------')

        keywords = summarize_with_keywords(sentences)
        print("키워드 추출 결과:")
        for word, r in sorted(keywords.items(), key=lambda x: x[1], reverse=True)[:30]:
            if r >= 1.0:
                print(f'{word:8s}:\t{r:.4f}')

        stopwords = split_string_to_array(quote)
        filtered_keywords = [word for word, score in keywords.items() if word not in stopwords and score >= 1.0]

        if len(filtered_keywords) > 1:    
            print("불용어 거른 키워드 추출 결과:")
            combined_keywords = ' '.join(filtered_keywords)
            print(combined_keywords)
            print('--------------------------')

            if combined_keywords:
                category = fetch_category_from_api(combined_keywords)
                categories.append(category)
                time.sleep(0.1)  # 각 요청 사이에 0.1초 대기

    write_categories_to_file(categories, output_filename)


if __name__ == "__main__":
    main()

# 58초