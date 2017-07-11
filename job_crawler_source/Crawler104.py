import requests as r
import sqlite3
import math
import time
import pprint
from bs4 import BeautifulSoup
import lxml
import threading

# index = "https://www.104.com.tw"

# 資訊軟體系統類
    # 軟體╱工程類人員 (12)
        # 軟體專案主管
        # 電子商務技術主管
        # 通訊軟體工程師
        # 軟體設計工程師
        # 韌體設計工程師
        # Internet程式設計師
        # 電腦系統分析師
        # 電玩程式設計師
        # 其他資訊專業人員
        # 資訊助理人員
        # BIOS工程師
        # 演算法開發工程師
    # MIS╱網管類人員 (8)
        # MIS╱網管主管
        # 資料庫管理人員
        # MIS程式設計師
        # MES工程師
        # 網路管理工程師
        # 系統維護╱操作人員
        # 資訊設備管制人員
        # 網路安全分析師

# job page list href (page1)
# https://www.104.com.tw/jobbank/joblist/joblist.cfm?cat=2007000000&jobsource=n104bank1&ro=0
# https://www.104.com.tw/jobbank/joblist/auto_joblist.cfm?auto=1&jobsource=n104bank1&ro=0&jobcat=2007000000&order=2&asc=0&page=1&psl=N_A

# job href selector
# soup.select('div.jobname_summary')[0].select('a')[0]['href']


# create table & drop table
with sqlite3.connect('job.sqlite') as conn:
    c = conn.cursor()
    try:
        c.execute('DROP TABLE job104')
        print('Drop Table job104')
    except:
        c.execute('''
            CREATE TABLE job104(
                jobID INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                href TEXT NOT NULL,
                times INTEGER,
                info TEXT)''')
        print('Create Table job104')


# number of total job
# 20 job hrefs in each page, but only get page 150
def getPage104(href):
    res = r.get(href)
    totalPages = int(BeautifulSoup(res.text, 'lxml').select('form#jobform')[0].select('ul')[0].select('li')[0].text.split('筆')[0][1:].strip())
    res.close()
    totalPages = 150 if math.ceil(totalPages / 20) > 150 else math.ceil(totalPages / 20)
    return totalPages


# sqlite insert&update -> job104
def insert_href(title, href):
    try:
        with sqlite3.connect('job.sqlite') as conn:

            # Query histry, whether we have insert it before...
            c = conn.cursor()
            qryString = "SELECT href FROM job104 where href=:href"
            c.execute(qryString, {'href' : href})
            # if there are nothing like href
            if len(c.fetchall()) == 0:
                # insert new one
                insert_string = "INSERT INTO job104 (title, href, times) VALUES (?, ?, 1)"
                c.execute(insert_string, (title, href))
            else:
                update_string = "UPDATE job104 SET times = times + 1 WHERE href = ?"
                c.execute(update_string, (href,))

    except ConnectionError as e:
        print(e)
        print(href)


# 資訊助理人員、演算法開發工程師
# getPage104('https://www.104.com.tw/jobbank/joblist/joblist.cfm?jobsource=n104bank1&ro=0&jobcat=2007001010%2C2007001012&order=3&asc=0&page=1')

# 資料庫管理人員
# getPage104('https://www.104.com.tw/jobbank/joblist/joblist.cfm?jobsource=n104bank1&ro=0&jobcat=2007002002&order=2&asc=0&page=1')

totalPages = getPage104('https://www.104.com.tw/jobbank/joblist/joblist.cfm?jobsource=n104bank1&ro=0&jobcat=2007000000&order=2&asc=0&page=1')
print('totalPages: ' + str(totalPages))
for page in range(1, totalPages + 1):
# for page in range(1, 86):
# all 
#     href = "https://www.104.com.tw/jobbank/joblist/joblist.cfm?jobsource=n104bank1&ro=0&jobcat=2007000000&order=3&asc=0&page={}".format(page)
# 軟體專案主管
#     href = "https://www.104.com.tw/jobbank/joblist/joblist.cfm?jobsource=n104bank1&ro=0&jobcat=2007001001&order=3&asc=0&page={}".format(page)
# 通訊軟體工程師
#     href = "https://www.104.com.tw/jobbank/joblist/joblist.cfm?jobsource=n104bank1&ro=0&jobcat=2007001003&order=3&asc=0&page={}".format(page)
# 韌體設計工程師
#    href = "https://www.104.com.tw/jobbank/joblist/joblist.cfm?jobsource=n104bank1&ro=0&jobcat=2007001005&order=3&asc=0&page={}".format(page)
# 電腦系統分析師
#    href = "https://www.104.com.tw/jobbank/joblist/joblist.cfm?jobsource=n104bank1&ro=0&jobcat=2007001007&order=3&asc=0&page={}".format(page)
# 其他資訊專業人員、BIOS工程師、電子商務技術主管
#     href = "https://www.104.com.tw/jobbank/joblist/joblist.cfm?jobsource=n104bank1&ro=0&jobcat=2007001009%2C2007001011%2C2007001002&order=3&asc=0&page={}".format(page)
# 資訊助理人員、演算法開發工程師
#    href = "https://www.104.com.tw/jobbank/joblist/joblist.cfm?jobsource=n104bank1&ro=0&jobcat=2007001010%2C2007001012&order=3&asc=0&page={}".format(page)
# 電玩程式設計師
#     href = "https://www.104.com.tw/jobbank/joblist/joblist.cfm?jobsource=n104bank1&ro=0&jobcat=2007001008&order=2&asc=0&page={}".format(page)
# Internet程式設計師
#     href = "https://www.104.com.tw/jobbank/joblist/joblist.cfm?jobsource=n104bank1&ro=0&jobcat=2007001006&order=3&asc=0&page={}".format(page)
# 軟體設計工程師 (經歷 多→少)
#     href = "https://www.104.com.tw/jobbank/joblist/joblist.cfm?jobsource=n104bank1&ro=0&jobcat=2007001004&order=3&asc=0&page={}".format(page)
# 軟體設計工程師 (經歷 少→多)
#    href = "https://www.104.com.tw/jobbank/joblist/joblist.cfm?jobsource=n104bank1&ro=0&jobcat=2007001004&order=3&asc=1&page={}".format(page)
# 軟體設計工程師 日期 新→舊
#    href = "https://www.104.com.tw/jobbank/joblist/joblist.cfm?jobsource=n104bank1&ro=0&jobcat=2007001004&order=2&asc=0&page={}".format(page)
# 軟體設計工程師 日期 舊→新
#     href = "https://www.104.com.tw/jobbank/joblist/joblist.cfm?jobsource=n104bank1&ro=0&jobcat=2007001004&order=2&asc=1&page={}".format(page)
# 軟體設計工程師 地區
#     href = "https://www.104.com.tw/jobbank/joblist/joblist.cfm?jobsource=n104bank1&ro=0&jobcat=2007001004&order=5&asc=0&page={}".format(page)
# 軟體設計工程師 相關性
#     href = "https://www.104.com.tw/jobbank/joblist/joblist.cfm?jobsource=n104bank1&ro=0&jobcat=2007001004&order=1&asc=0&page={}".format(page)
# 軟體設計工程師 學歷 高→低
#     href = "https://www.104.com.tw/jobbank/joblist/joblist.cfm?jobsource=n104bank1&ro=0&jobcat=2007001004&order=4&asc=0&page={}".format(page)
# 軟體設計工程師 學歷 低→高
#     href = "https://www.104.com.tw/jobbank/joblist/joblist.cfm?jobsource=n104bank1&ro=0&jobcat=2007001004&order=4&asc=1&page={}".format(page)
# 軟體設計工程師 應徵人數 高→低
#     href = "https://www.104.com.tw/jobbank/joblist/joblist.cfm?jobsource=n104bank1&ro=0&jobcat=2007001004&order=7&asc=0&page={}".format(page)
# 軟體設計工程師 應徵人數 低→高
#    href = "https://www.104.com.tw/jobbank/joblist/joblist.cfm?jobsource=n104bank1&ro=0&jobcat=2007001004&order=7&asc=1&page={}".format(page)
# 軟體設計工程師 待遇 高→低
#     href = "https://www.104.com.tw/jobbank/joblist/joblist.cfm?jobsource=n104bank1&ro=0&jobcat=2007001004&order=6&asc=1&page={}".format(page)
# 軟體設計工程師 待遇 低→高
#     href = "https://www.104.com.tw/jobbank/joblist/joblist.cfm?jobsource=n104bank1&ro=0&jobcat=2007001004&order=6&asc=0&page={}".format(page)
# Internet程式設計師 日期 舊→新
#     href = "https://www.104.com.tw/jobbank/joblist/joblist.cfm?jobsource=n104bank1&ro=0&jobcat=2007001006&order=2&asc=1&page={}".format(page)
# Internet程式設計師 日期 新→舊
#     href = "https://www.104.com.tw/jobbank/joblist/joblist.cfm?jobsource=n104bank1&ro=0&jobcat=2007001006&order=2&asc=0&page={}".format(page)
# MIS╱網管主管、網路管理工程師、資訊設備管制人員
#     href = "https://www.104.com.tw/jobbank/joblist/joblist.cfm?jobsource=n104bank1&ro=0&jobcat=2007002001%2C2007002005%2C2007002007&order=2&asc=0&page={}".format(page)
# MIS程式設計師
#     href = "https://www.104.com.tw/jobbank/joblist/joblist.cfm?jobsource=n104bank1&ro=0&jobcat=2007002003&order=2&asc=0&page={}".format(page)
# MES工程師、系統維護╱操作人員、網路安全分析師
#     href = "https://www.104.com.tw/jobbank/joblist/joblist.cfm?jobsource=n104bank1&ro=0&jobcat=2007002004%2C2007002006%2C2007002008&order=2&asc=0&page={}".format(page)
# 資料庫管理人員
#     href = "https://www.104.com.tw/jobbank/joblist/joblist.cfm?jobsource=n104bank1&ro=0&jobcat=2007002002&order=2&asc=0&page={}".format(page)

    soup = BeautifulSoup(r.get(href).text, 'lxml')
    jidSoup = soup.select('div.job_name')
    totalJid = len(jidSoup)
    if page % 10 == 0:
        print(str(page) + ' / ' + str(totalPages))
    for jid in range(0, totalJid):
        title = soup.select('div.job_name')[jid].text.strip()
        href = "https://www.104.com.tw" + jidSoup[jid].select('a')[0]['href']
        insert_href(title, href)
    
    time.sleep(1)
    
print('done!!')


# Query result program
with sqlite3.connect('job.sqlite') as conn:
    c = conn.cursor()
    pprint.pprint(list(c.execute('select * from job104')))


# Query maximun times
with sqlite3.connect('job.sqlite') as conn:
    c = conn.cursor()
#     pprint.pprint(list(c.execute('select * from job104 where times > 1')))
    pprint.pprint(list(c.execute('select count(times), sum(times) from job104 where times > 1')))


# ranking function
# ranking = sorted(dict.items(),key=lambda d:d[1],reverse = True) #用出現次數排順序
