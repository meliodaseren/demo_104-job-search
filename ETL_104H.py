# catch job title and url

import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver

browser = webdriver.Chrome('./chromedriver')
browser.maximize_window()

url = 'https://www.104.com.tw/jobbank/joblist/joblist.cfm?cat=2007000000&jobsource=n104bank1&ro=0'
page = 1

while True:
    browser.get(url)
    soup = BeautifulSoup(browser.page_source, 'lxml')
    # tmp1 = soup.select('li > div > a')[4:] #li > div > a
    # print(browser.find_element('li > div > a'))
    tmp = soup.findAll(attrs={'class': 'jobname_summary job_name'})
    count = 1
    url_ti = 'https://www.104.com.tw'
    for ti in tmp:
        print(count, ti.text.strip(), '\t', url_ti + str(ti).split("a href=\"")[1].split("\"")[0])
        count += 1
    page = page + 1
    # url = 'https://www.104.com.tw/jobbank/joblist/joblist.cfm?jobsource=n104bank1&ro=0&jobcat=2007000000&order=2&asc=1&page=' + str(page)
    # url = 'https://www.104.com.tw/jobbank/joblist/auto_joblist.cfm?auto=1&jobsource=n104bank1&ro=0&jobcat=2007000000&order=2&asc=0&page=' + str(page)
    url = 'https://www.104.com.tw/jobbank/joblist/joblist.cfm?jobsource=n104bank1&ro=0&jobcat=2007000000&order=2&asc=1&page=' + str(page)

    time.sleep(3)