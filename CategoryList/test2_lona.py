import os

def process_file(file_path, output_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # 각 줄의 양쪽 공백 제거 및 '/' 기준으로 나누기
    processed_lines = []
    for line in lines:
        stripped_line = line.strip()
        if '/' in stripped_line:
            parts = stripped_line.split('/')
            processed_lines.extend(parts)
        else:
            processed_lines.append(stripped_line)

    # 중복 제거
    unique_lines = list(dict.fromkeys(processed_lines))

    # 가나다 순으로 정렬
    unique_lines.sort()

    with open(output_path, 'w', encoding='utf-8') as file:
        file.write('\n'.join(unique_lines))

input_file = r'C:\Users\aaron\OneDrive\Desktop\SIG\workspace\2024_Summer_SIG-main\CategoryList\input.txt'  # 원본 파일 경로
output_file = r'C:\Users\aaron\OneDrive\Desktop\SIG\workspace\2024_Summer_SIG-main\CategoryList\output.txt' # 결과를 저장할 파일 경로
process_file(input_file, output_file)