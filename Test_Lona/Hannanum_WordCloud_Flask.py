import urllib.request
import urllib.parse
import requests
from bs4 import BeautifulSoup
import re
import json
import time

from konlpy.tag import Hannanum
from krwordrank.word import summarize_with_keywords
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt


def make_wordcloud(user_request):
    # 초기 설정
    hannanum=Hannanum()

    client_id = "_C12LIJCwlme2ozPrU3k"  # 네이버 오픈 API ID
    client_secret = "Gehzb9ohra"  # 네이버 오픈 API secret

    # 검색어 입력 받기
    user_request = user_request
    print(hannanum.nouns(user_request))
    quote = ' '.join(hannanum.nouns(user_request))
    encText = urllib.parse.quote(quote)
    display_num = 100

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

    body = response_body.decode('utf-8')
    body = body.replace('"', '')
    list1 = body.split('\n\t\t{\n\t\t\t')
    list1 = [i for i in list1 if 'naver' in i]

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
    def split_noun_sentences(text):
        sentences = text.replace(". ", ".")
        sentences = re.sub(r'([^\n\s\.\?!]+[^\n\.\?!]*[\.\?!])', r'\1\n', sentences).strip().split("\n")
        result = []
        for sentence in sentences:
            if len(sentence) == 0:
                continue
            sentence_pos = hannanum.pos(sentence)
            nouns = [word for word, pos in sentence_pos if pos == 'N' or pos == 'NB' or pos =='NC' or pos =='NQ']
            if len(nouns) == 1:
                continue
            result.append(' '.join(nouns) + '.')
        return result
# 본문 추출 및 문장 단위로 쪼개기
    for i in noneIframe_url:
        res = requests.get(i, headers=headers)
        html = BeautifulSoup(res.text, "html.parser")

        div = html.find('div', class_='se-main-container')
        if not div:
            continue
        content = preprocess_sentence_kr(div.text.replace('\n', ''))
        contents.append(content)

# 키워드 추출 및 카테고리 가져오기
    output_filename = r'./HannanumList.txt'

    def clean_category(category):
        return category.replace('기타', '').replace('여성', '').replace('남성', '').replace('데코용품', '').replace('스티커', '').replace('케이크토퍼', '').strip()
    def fetch_category_from_api(keywords):
        encText = urllib.parse.quote(keywords)
        url = "https://openapi.naver.com/v1/search/shop?query=" + encText + "&display=1&start=1"  # JSON 결과
        request = urllib.request.Request(url)
        request.add_header("X-Naver-Client-Id", client_id)
        request.add_header("X-Naver-Client-Secret", client_secret)

        retries = 5
        for i in range(retries):
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
                        return clean_category(category)
                    return 'NO items'
                return f"Error Code: {response.getcode()}"
    def write_categories_to_file(categories, output_filename):
        filtered_categories = [category for category in categories if category != 'NO items']
        category_counter = Counter(filtered_categories)
        sorted_categories = sorted(category_counter.items(), key=lambda item: item[1], reverse=True)

        with open(output_filename, 'w', encoding='utf-8') as output_file:
            for category, count in sorted_categories:
                output_file.write(f"{clean_category(category)} {count}\n")

    def generate_wordcloud(categories):
        category_counter = Counter(categories)

        wordcloud = WordCloud(width=400, height=400, background_color='white', font_path='C:/Windows/Fonts/malgun.ttf').generate_from_frequencies(category_counter)
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.savefig('./static/wordcloud.png')

        keyword_frequencies = Counter()
    def main():
        categories = []
        for content in contents:
            sentences = split_noun_sentences(content)

            try:
                keywords = summarize_with_keywords(sentences)
            except Exception as e:
                print(f"키워드 추출 오류: {e}")
                continue

            stopwords = split_string_to_array(quote)
            filtered_keywords = [word for word, score in keywords.items() if word not in stopwords and score >= 1.0]

            if len(filtered_keywords) > 1:
                combined_keywords = ' '.join(filtered_keywords)

                if combined_keywords:
                    category = fetch_category_from_api(combined_keywords)
                    if category != 'NO items':
                        categories.append(category)
                    time.sleep(0.1)  # 각 요청 사이에 0.1초 대기

        write_categories_to_file(categories, output_filename)
        generate_wordcloud(categories)

    main()