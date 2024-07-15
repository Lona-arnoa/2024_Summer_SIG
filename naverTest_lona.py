import urllib.request

# 발급받은 클라이언트 ID와 시크릿
client_id = "iawHez84A3yMNs5YGK0I"
client_secret = "oIzCC77Y4m"

category_list = [each['category2'] for each in json_result['items']]
set(category_list)