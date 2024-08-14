from konlpy.tag import Kkma
from konlpy.tag import Okt
from konlpy.tag import Hannanum
from konlpy.tag import Komoran

# 초기 설정
okt = Okt()
kkma=Kkma()
hannanum = Hannanum()
komoran = Komoran()

# 꼬꼬마 명사 추출
print('kkma 명사 추출: ',kkma.nouns('추석 때 부모님께 드릴 선물 추천해줘'))

# Okt 명사 추출
print('Okt 명사 추출: ', okt.nouns('추석 때 부모님께 드릴 선물 추천해줘'))

# Hannanum 명사 추출
print('Hannanum 명사 추출: ', hannanum.nouns('추석 때 부모님께 드릴 선물 추천해줘'))

# Komoran 명사 추출
print('komoran 명사 추출: ', komoran.nouns('추석 때 부모님께 드릴 선물 추천해줘'))

# 꼬꼬마 명사 추출
print('kkma 명사 추출: ',kkma.nouns('고등학생 동생이 곧 졸업하는데 선물 추천해줘'))

# Okt 명사 추출
print('Okt 명사 추출: ', okt.nouns('고등학생 동생이 곧 졸업하는데 선물 추천해줘'))

# Hannanum 명사 추출
print('Hannanum 명사 추출: ', hannanum.nouns('고등학생 동생이 곧 졸업하는데 선물 추천해줘'))

# Komoran 명사 추출
print('komoran 명사 추출: ', komoran.nouns('고등학생 동생이 곧 졸업하는데 선물 추천해줘'))