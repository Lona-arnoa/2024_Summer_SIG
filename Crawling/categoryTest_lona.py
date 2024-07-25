import urllib.request
import urllib.parse
import json
from collections import Counter

client_id = "iawHez84A3yMNs5YGK0I"
client_secret = "oIzCC77Y4m"
input_filename = r'C:\Users\aaron\OneDrive\Desktop\SIG\workspace\2024_Summer_SIG-main\Crawling\ResultList.txt'
output_filename = r'C:\Users\aaron\OneDrive\Desktop\SIG\workspace\2024_Summer_SIG-main\Crawling\FinalList.txt'

def read_words_from_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        words = file.read().splitlines()
    return words

def fetch_category_from_api(word):
    encText = urllib.parse.quote(word)
    url = f"https://openapi.naver.com/v1/search/shop?query={encText}"  # JSON 결과
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", client_id)
    request.add_header("X-Naver-Client-Secret", client_secret)
    try:
        with urllib.request.urlopen(request) as response:
            if response.getcode() == 200:
                response_json = json.loads(response.read().decode('utf-8'))
                items = response_json.get('items', [])
                if items:
                    first_item = items[0]
                    # 카테고리 우선순위: category4 > category3 > category2
                    category4 = first_item.get('category4', '').strip()
                    category3 = first_item.get('category3', '').strip()
                    category2 = first_item.get('category2', '').strip()
                    
                    if category4:
                        return category4
                    elif category3:
                        return category3
                    elif category2:
                        return category2
                    else:
                        return 'No category2, category3, or category4'
                return 'No items found'
            return f"Error Code: {response.getcode()}"
    except Exception as e:
        return f"Error fetching data: {e}"

def write_categories_to_file(categories, output_filename):
    # 카테고리 빈도 계산
    category_counter = Counter(categories)
    # 빈도수로 정렬 (빈도가 높은 순서대로)
    sorted_categories = sorted(category_counter.items(), key=lambda item: item[1], reverse=True)
    
    with open(output_filename, 'w', encoding='utf-8') as output_file:
        for category, count in sorted_categories:
            output_file.write(f"{category} {count}\n")

def main():
    # 입력 파일에서 단어를 읽어옴
    words = read_words_from_file(input_filename)

    # 상위 20개 단어만 처리
    top_words = words[:20]
    
    # 각 단어에 대해 카테고리 가져오기
    categories = [fetch_category_from_api(word) for word in top_words]
    
    # 카테고리 빈도수에 따라 정렬하고 출력 파일에 저장
    write_categories_to_file(categories, output_filename)

if __name__ == "__main__":
    main()