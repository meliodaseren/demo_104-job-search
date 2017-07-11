
# coding: utf-8

# # ETL作業第三階段
# 
# 拆字

# In[1]:

# 功能:
# 從目前工作資料夾的資料庫中取出網址以及內容
# 然後新建一個資料庫
# 分析完內容有哪些程式語言後
# 將結果以布林值儲存在新建的資料庫裡

# 使用者只需修改source, source_table以及db_name
# 確認db_name與資料夾裡的其他檔案名稱沒有重複
# 就可以按Kernel -> Restart & Run All執行

# 請先將job104p1, p2, p3, job518或job1111.sqlite放到目前資料下
# 為來源(source)的資料庫以及表格命名

source = "job104p1.sqlite"
source_table = "job104"

# 儲存結果的資料庫的名稱
# 可自訂

db_name = source.replace(".sqlite","") + "_result.sqlite"


# In[2]:

# 準備工作

# 引用所有會用到的套件

from bs4 import BeautifulSoup
import requests
import bs4
import time
import re
import sqlite3
import sys
import copy


# In[3]:

# 建立程式語言字典

lang_dict = {
"csharp" : ["c#", "visual c#", "c sharp", "net c#", "cs", "csharp"],
"cpp" : ["visual c++", "c++", "cpp"],
"vb" : ["visual basic", "vb", "visualbasic"],
"vba" : ["visual basic application", "vba"],
"vbnet" : ["vb.net", "visual basic.net"],
"aspnet" : ["asp.net", "asp c#.net ", "asp vb.net", "aspnet", "asp .net"],
"c" : ["c"],
"java" : ["java", "jsp", "severlet", "j2se", "j2ee", "jse"],
"fsharp" : ["f#", "f sharp", "fsharp"],
"objective_c" : ["objective-c"],
"swift" : ["swift"],
"php" : ["php"],
"python" : ["python"],
"perl" : ["perl"],
"ruby" : ["ruby", "ruby on rails", "rubyonrails", "ruby-on-rails"],
"go" : ["go"],
"vbscript" : ["vbscript", "vb script"],
"typescript" : ["typescript"],
"coffeescript" : ["coffeescript"],
"scala" : ["scala"],
"r" : ["r"],
"applescript" : ["applescript"],
"pascal" : ["pascal"],
"cobol" : ["cobol"],
"html" : ["html", "css", "javascript", "js", "jquery", "rwd"],
"matlab" : ["matlab"],
"sql" : ["sql", "Oracle", "ssms", "db2", "rdb", "relational database"],
"kaskell" : ["kaskell"],
"nodejs" : ["nodejs", "node.js", "node js"],
"angular" : ["angular", "angular.js", "angular js"],
"asp" : ["asp"],
"assembly" : ["assembly"],
"delphi" : ["delphi"]
}

# 先將lang_dict的value轉為小寫

for key in lang_dict:
    lang_dict.update({key: [x.lower() for x in lang_dict[key]]})

# 把lang_dict的key另外存成list
    
lang_dict_keys = list(lang_dict.keys())


# 建立lang_list與lang_dict_inv
# lang_list結合所有的程式語言名稱
# 而lang_dict_inv紀錄某個名字所指的是哪個程式語言

lang_list = []
lang_dict_inv = {}

for key in list(lang_dict):
    for each in lang_dict[key]:
        lang_list.append(each)
        lang_dict_inv.update({each:key})

        
# 由字串長度將lang_list的內容最長排到最短
# (這步很重要)

lang_list.sort(key = lambda s: -len(s))


# lang_list_nospace
# 無空格版的lang_list

lang_list_nospace = [x.replace(" ","") for x in lang_list]


# In[4]:

# 從source取得href以及info

with sqlite3.connect(source) as conn:
    c = conn.cursor()
    c.execute("SELECT href, info from " + source_table + ";")
    input_pairs = c.fetchall()


# In[5]:

# 建立儲存資料用的sqlite資料庫

# 產出指令

columns = ""
for each in lang_dict_keys:
    columns += ", " + each + " BOOLEAN NOT NULL DEFAULT 0 "

# 建立

with sqlite3.connect(db_name) as conn:
    c = conn.cursor()
    c.execute("CREATE TABLE result(href TEXT NOT NULL UNIQUE " + columns + ");")


# In[6]:

# 定義lang_parse方法

# 尋找某個語言是否有在一個字串中被提到
# 以刪除法排除沒有的字串 剩下的就是有被提到的

def lang_parse(info):
    
    # 階段1

    # 轉成小寫
    info_lower = info.lower()

    # 移除info_lower中的空白
    info_nospace = info_lower.replace(" ","")

    # 階段2

    # 複製出一個消耗性的lang_list_copy
    # 依序尋找語言名稱
    # 看該語言在不在lang_list_nospace_copy裡面
    # 如果在就找info_copy的下一個語言名稱
    # 不在的話就將該語言名稱從info_copy
    # 跟info_nospace_copy中刪除
    # 然後將該名稱從info_nospace刪除
    # 以避免有子字串摻雜的現象

    # 因為上面在做準備工作的時候有將lang_list_nospace
    # 依照字串長度從常到短排序
    # 所以不會有誤刪母字串的情形發生

    lang_list_copy = list(lang_list)
    lang_list_nospace_copy = list(lang_list_nospace)

    i = 0
    while i < len(lang_list_nospace_copy) and len(info_nospace) > 0:
        exists = lang_list_nospace_copy[i] in info_nospace
        info_nospace = info_nospace.replace(lang_list_nospace_copy[i],"")
        if exists:
            i += 1
        else:
            del lang_list_nospace_copy[i] # 這個要做才能避免無限迴圈
            del lang_list_copy[i]  # 讓lang_list_copy同步

    # 階段3

    # 再回頭來看info_lower
    # 用正規表示法尋找語言名稱
    # 但如果lang_list_copy已經全軍覆沒就略過不做
    
    if(len(lang_list_copy) > 0):
        i = 0
        while i < len(lang_list_copy):
            lang_name = lang_list_copy[i]
            if " " not in lang_name:
                lang_name = lang_name.replace("+","\+")  # 跳脫符號
                lang_name = "(^|[^a-zA-Z])" + lang_name +"($|[^a-zA-Z])" # 正規表示法
                query = re.compile(lang_name)
                exists = not (query.search(info_lower) == None )
                if exists:
                    i += 1
                else:
                    del lang_list_copy[i]
            else:
                i += 1
    
    # 階段4

    # 建立集合lang_exists
    # 用來紀錄那些語言存在
    # (順序不重要)

    lang_exists = set()
    
    # 將找到的結果利用lang_dict_inv
    # 紀錄到lang_exists裡
    # 但如果lang_list_copy已經全軍覆沒就略過不做
    
    if(len(lang_list_copy) > 0):
        for each in lang_list_copy:
            lang = lang_dict_inv[each]
            lang_exists.add(lang)  
    
    # 傳回lang_exists
            
    return lang_exists


# In[7]:

# 定義insert_parse方法
# 將lang_parse的結果儲存到資料庫上

def insert_parse(href, lang_exists):
    
    cols = ""
    vals = ""
    
    if(len(lang_exists) > 0):
        for each in lang_exists:
            cols += "," + each
            vals += ", 1"      
    
    command = "INSERT INTO result (href" + cols + ")         values('" + href + "'" + vals + ");"
    
    with sqlite3.connect(db_name) as conn:
        c = conn.cursor() 
        c.execute(command)


# In[8]:

# 開始跑

for each in input_pairs:
    
    # 重設href跟lang_exists以避免迴圈重作
    
    href = ""
    lang_exists = set()
    
    try:
        href = each[0]
        lang_exists = lang_parse(each[1])
        insert_parse(href,lang_exists)
        print(lang_exists)
    except:
        print("錯誤於" + href + ": ", sys.exc_info()[1])


# In[9]:

# 檢查部份結果

with sqlite3.connect(db_name) as conn:
        c = conn.cursor() 
        c.execute("select count(*) from result;")
        output = c.fetchall()
print(output)

