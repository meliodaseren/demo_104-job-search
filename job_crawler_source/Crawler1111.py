import requests as r
import sqlite3
import math
import time
import pprint
from bs4 import BeautifulSoup
import lxml
import threading


index = "https://www.1111.com.tw/job-bank/job-index.asp?si=1&d0=140200,140300,140400,140100&fs=1&ps=100&page=2"
#        https://www.1111.com.tw/job-bank/job-index.asp?si=1&d0=140200,140300,140400,140100&fs=1&page=2


# create table & drop table
with sqlite3.connect('job.sqlite') as conn:
    c = conn.cursor()
    try:
        c.execute('drop table job1111')
        print('drop table job1111')
    except:
        c.execute('''
            CREATE TABLE job1111(
              jobID INTEGER PRIMARY KEY AUTOINCREMENT,
              title TEXT NOT NULL,
              href TEXT NOT NULL,
              times INTEGER,
              info TEXT)''')
        print('create table job1111')


# number of total job 
def getPage1111(href):
#     import locale
#     locale.setlocale(locale.LC_ALL, 'en_US.UTF-8') 
    res = r.get(href)
    
    return int(BeautifulSoup(res.text, 'lxml').select('div.pagedata')[0].text.split('頁')[0].split('/')[1].strip())

totalPages = getPage1111(index)
totalPages


res = r.get(index)
soup = BeautifulSoup(res.text, 'lxml').select('div#jobResult > ul')


# test program -> get href
soup[0].select('div.jbInfoin')[0].select('a')[0]['href'][2:]


# sqlite insert&update -> job1111
def insert_href(title, href):
    try:
        with sqlite3.connect('job.sqlite') as conn:

            # Query histry, whether we have insert it before...
            c = conn.cursor()
            qryString = "SELECT href FROM job1111 where href=:href"
            c.execute(qryString, {'href' : href})
            # if there are nothing like href
            if len(c.fetchall()) == 0:
                # insert new one
                insert_string = "INSERT INTO job1111 (title, href, times) VALUES (?, ?, 1)"
                c.execute(insert_string, (title, href))
            else:
                update_string = "UPDATE job1111 SET times = times + 1 WHERE href = ?"
                c.execute(update_string, (href,))

    except ConnectionError as e:
        print(e)
        print(href)


# main program
for page in range(1, totalPages + 1):
# for page in range(1, 2):
    href = "https://www.1111.com.tw/job-bank/job-index.asp?si=1&d0=140200,140300,140400,140100&fs=1&ps=100&page={}".format(page)
    soup = BeautifulSoup(r.get(href).text, 'lxml')
    jidSoup = soup.select('div.jbInfo > div')
    totalJid = len(jidSoup)
    print('page: ' + str(page))
    for jid in range(0, totalJid):
        title = jidSoup[jid].select('h3')[0].text
        href = jidSoup[jid].select('a')[0]['href'][2:]
        insert_href(title, href)
    
    # time.sleep(2)
res.close()
print('done!!')


res.close()


# Query result program
# 2017/05/08 : ? web(exclude repeat)
with sqlite3.connect('job.sqlite') as conn:
    c = conn.cursor()
    pprint.pprint(list(c.execute('select * from job1111')))


# Query maximun times
with sqlite3.connect('job.sqlite') as conn:
    c = conn.cursor()
#     pprint.pprint(list(c.execute('select * from job1111 where times > 1')))
    pprint.pprint(list(c.execute('select count(times), sum(times) from job1111 where times > 1')))
