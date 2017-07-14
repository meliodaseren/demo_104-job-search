import string
import json
from collections import Counter

import jieba
from jieba.analyse import extract_tags

jieba.set_dictionary('./extra_dict/dict.txt.big')

# 設定要切割的全型特殊字符
strip_set = '，•。、﹐．﹒˙·‥…‧？！－｜＝＋／＼︿＊＄＆％＃＠〃；﹔︰﹕：～′‵〝〞‘’（）＜＞《》｛｝［］『』「」“”❞❝﹁﹂﹃﹄»＂'

with open('./dataset/zhihu_ml.txt', encoding = 'utf8') as zhihu:
    zhihu_ml = zhihu.read()
    # print(zhihu_ml)

wd_count = Counter()
for word in jieba.cut(zhihu_ml):
    # 切割出數字、字母、標點符號、空白字符
    word = word.strip(string.printable).strip(strip_set)
    # print(word)
    if word in wd_count:
        wd_count[word] += 1
    else:
        wd_count[word] = 1

# print(len(wd_count))
# print(wd_count)
print(wd_count.most_common())

print('--' * 50)

# Jieba 基於 TF-IDF 算法的關鍵字抽取
print(extract_tags(zhihu_ml))

print('--' * 50)