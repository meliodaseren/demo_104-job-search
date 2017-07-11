import requests as r
import sqlite3
import math
import time
import pprint
from bs4 import BeautifulSoup
import lxml
import threading


index = "https://www.518.com.tw/job-index-P-1.html?i=1&am=1&ab=2032001,2032002,"
#        https://www.518.com.tw/job-index-P-1.html?i=1&am=1&ab=2032001,2032002,


# create table & drop table
with sqlite3.connect('job.sqlite') as conn:
    c = conn.cursor()
    try:
        c.execute('drop table job518')
        print('drop table job518')
    except:
        c.execute('''
            CREATE TABLE job518(
              jobID INTEGER PRIMARY KEY AUTOINCREMENT,
              title TEXT NOT NULL,
              href TEXT NOT NULL,
              times INTEGER,
              info TEXT)''')
        print('create table job518')


# number of total job 
def getPage1111(href):
#     import locale
#     locale.setlocale(locale.LC_ALL, 'en_US.UTF-8') 
    res = r.get(href)
    
    return int(BeautifulSoup(res.text, 'lxml').select('span.pagecountnum')[0].text.split('頁')[0].split('/')[1].strip())

totalPages = getPage1111(index)


res = r.get(index)
soup = BeautifulSoup(res.text, 'lxml').select('div#listContent')


# test program -> get href
soup[0].select('a')[0]['href'][0:]


# sqlite insert&update -> job518
def insert_href(title, href):
    try:
        with sqlite3.connect('job.sqlite') as conn:

            # Query histry, whether we have insert it before...
            c = conn.cursor()
            qryString = "SELECT href FROM job518 where href=:href"
            c.execute(qryString, {'href' : href})
            # if there are nothing like href
            if len(c.fetchall()) == 0:
                # insert new one
                insert_string = "INSERT INTO job518 (title, href, times) VALUES (?, ?, 1)"
                c.execute(insert_string, (title, href))
            else:
                update_string = "UPDATE job518 SET times = times + 1 WHERE href = ?"
                c.execute(update_string, (href,))

    except ConnectionError as e:
        print(e)
        print(href)


# main program
for page in range(1, totalPages + 1):
# for page in range(1, 2):
    href = "https://www.518.com.tw/job-index-P-{}.html?i=1&am=1&ab=2032001,2032002,".format(page)
    soup = BeautifulSoup(r.get(href).text, 'lxml')
    jidSoup = soup.select('div#listContent > ul')
    totalJid = len(jidSoup)
    print(totalJid)
    print('page: ' + str(page))
    for jid in range(0, totalJid-3):
        title = jidSoup[jid].select('a')[0]['title'][0:].split('職缺名：')[1].split('\n')[0]
        href = jidSoup[jid].select('a')[0]['href'][0:].replace(' ','')
        print(title)
        print(href)
        insert_href(title, href)
    for jid in range(totalJid-3, totalJid):
        title = jidSoup[jid].select('a')[0]['title'][0:]
        href = jidSoup[jid].select('a')[0]['href'][0:].replace(' ','')
        print(title)
        print(href)
        insert_href(title, href)
    
#     time.sleep(2)
res.close()
print('done!!')


res.close()


# Query result program
# 2017/05/08 : ? web(exclude repeat)
with sqlite3.connect('job.sqlite') as conn:
    c = conn.cursor()
    pprint.pprint(list(c.execute('select * from job518')))


# Query maximun times
with sqlite3.connect('job.sqlite') as conn:
    c = conn.cursor()
#     pprint.pprint(list(c.execute('select * from job1111 where times > 1')))
    pprint.pprint(list(c.execute('select count(times), sum(times) from job518 where times > 1')))
