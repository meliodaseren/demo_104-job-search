import json
import requests
import datetime as dt # import with an alias name
from collections import Counter as Ctr # import submodule at top level namespace with an alias

import jieba
from jieba.analyse import extract_tags

def str2dict(data_str):
    data = {}
    for row in data_str.split('\n'):
        kv_list = row.split(":")
        data[kv_list[0]] = kv_list[1]
    return data

data_str = """method:search
searchMethod:true
searchTarget:ATM
orgName:
orgId:
hid_1:1
tenderName:
tenderId:
tenderStatus:4,5,21,29
tenderWay:
awardAnnounceStartDate:106/06/28
awardAnnounceEndDate:106/06/28
proctrgCate:
tenderRange:
minBudget:
maxBudget:
item:
hid_2:1
gottenVendorName:
gottenVendorId:
hid_3:1
submitVendorName:
submitVendorId:
location:
execLocationArea:
priorityCate:
isReConstruct:
btnQuery:查詢"""

data = str2dict(data_str)

res = requests.post("http://web.pcc.gov.tw/tps/pss/tender.do?searchMode=common&searchType=advance", data=data)