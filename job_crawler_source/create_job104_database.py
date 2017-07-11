# # 建立job104p1, job104p2跟job104p3 sqlite資料庫的程式


# 在目前所在的位置建立資料庫
# 預備存放從網站爬下來的資料

# 建立前請依需求將所有的p*改成p1,p2或p3
# 然後跑步驟1~5
# (步驟2如果要重作得先刪除資料夾中同名的檔案)


# 第1步驟
# 套用sqlite3套件

import sqlite3


# 第2步驟

# 請在當下資料夾沒有job104p*的時候執行

# 建立job104p1.sqlite資料庫
# 若要建立p2跟p3只要改db_name即可

#db_name = "job104p1.sqlite"
db_name = "job104p2.sqlite"
# db_name = "job104p3.sqlite"

with sqlite3.connect(db_name) as conn:
    c = conn.cursor()
    c.execute("""CREATE TABLE job104(
    href TEXT NOT NULL UNIQUE,
    info TEXT NOT NULL,
    lang TEXT)""")

conn.close()


# 第3步驟
# 塞入所有的href資料作為primary key
# 依照p1, p2或p3用不同的指令,如下

href_source = "job.sqlite"

with sqlite3.connect(href_source) as conn2:

    c2 = conn2.cursor()

#   p1用:
    #qrystring_source = "SELECT href from job104 where jobID <= 6300;"

#   p2用:
    qrystring_source = "SELECT href from job104 where jobID > 6300 and jobID <= 12600;"

#   p3用:
#    qrystring_source = "SELECT href from job104 where jobID > 12600;"

    c2.execute(qrystring_source)
    href_list = c2.fetchall()
    
conn2.close()


# 第4步驟
# 將href從job104轉移到job104p1
# 依照p1, p2或p3用不同的指令,如下

#href_dest = "job104p1.sqlite"
href_dest = "job104p2.sqlite"
# href_dest = "job104p3.sqlite"

with sqlite3.connect(href_dest) as conn3:
    
    c3 = conn3.cursor()
    
    for each in href_list:
        
        qryString_dest = "INSERT INTO job104 (href, info) VALUES(?, ?);"
        c3.execute(qryString_dest,[each[0],""])

conn3.close()


# 第5步驟
# 檢查結果
# 依照p1, p2或p3用不同的指令,如下

import pprint

#with sqlite3.connect('job104p1.sqlite') as conn: 
with sqlite3.connect('job104p2.sqlite') as conn: 
# with sqlite3.connect('job104p3.sqlite') as conn: 
    c = conn.cursor()
    result = list(c.execute('select * from job104;'))
    pprint.pprint(result)
    
conn.close()
