from konlpy.tag import Kkma
kkma=Kkma()
#형태소 분석
print(kkma.morphs('안녕. 나는 하늘색과 딸기를 좋아해'))

#명사 추출
print(kkma.nouns('안녕. 나는 하늘색과 딸기를 좋아해'))

#품사와 함께 반환
print(kkma.pos('안녕. 나는 하늘색과 딸기를 좋아해'))

#문장 추출
print(kkma.sentences('안녕하세요. 나는 하늘색과 딸기를 좋아해'))