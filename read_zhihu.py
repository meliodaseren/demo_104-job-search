import json
from collections import Counter

import jieba
from jieba.analyse import extract_tags

jieba.set_dictionary('./extra_dict/dict.txt.big')

with open('./dataset/zhihu_ml.txt', encoding = 'utf8') as zhihu:
    zhihu_ml = zhihu.read()
    print(zhihu_ml)

jieba.cut(zhihu_ml)

wd_count = Counter()
