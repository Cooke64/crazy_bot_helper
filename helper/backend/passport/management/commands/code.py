import json

import pandas as pd
from urllib.request import Request, urlopen

url = 'http://www.consultant.ru/document/cons_doc_LAW_126897/'


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}
req = Request(url, headers=headers)
webpage = urlopen(req).read()

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', 0)

data = pd.read_html(webpage, )[0]
list_dict = []

for index, row in list(data.iterrows()):
    list_dict.append(dict(row))
with open("passport_types.json", 'w', encoding='utf-8') as file:
    json.dump(list_dict[0], file, ensure_ascii=False, sort_keys=False, indent=4)
with open("data.json", 'w', encoding='utf-8') as file:
    json.dump(list_dict[1:], file, ensure_ascii=False, sort_keys=False, indent=4)
