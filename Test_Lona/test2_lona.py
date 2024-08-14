# from konlpy.tag import Okt
# okt = Okt()

# text = "20대 남성에게 추천할 선물이 있을까?"

# print(okt.morphs(text))
# print(okt.morphs(text, stem=True))
# print(okt.nouns(text))

from konlpy.tag import Hannanum

hannanum = Hannanum()

print(hannanum.nouns(u'20대 남성에게 추천할 선물이 있을까?'))
print(hannanum.nouns(u'추석때 부모님께 드릴 선물을 추천해줘'))
print(hannanum.nouns(u'내 친구 한승현의 취업 선물을 추천해줘'))