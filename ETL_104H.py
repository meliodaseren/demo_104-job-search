from selenium import webdriver
from bs4 import BeautifulSoup as bs
from selenium.webdriver.support.select import Select
import requests
import time
browser = webdriver.Chrome('E://PycharmProjects/selenium_driver/chromedriver')
browser.maximize_window()

url = 'https://www.104.com.tw/jobbank/joblist/joblist.cfm?\
       indcat=1001001002&area=6001001000&jobsource=104_bank1'
page = 1
while True:
    browser.get(url)
    soup = bs(browser.page_source, 'lxml')
    # tmp1 = soup.select('li > div > a')[4:] #li > div > a
    # print(browser.find_element('li > div > a'))
    tmp2 = soup.findAll(attrs={"class": "jobname_summary job_name"})
    tmp3 = tmp2
    count = 1
    for ti in tmp3:
        # print(c,xx.text.strip())
        print(count, ti.text.strip(), "\t", str(ti).split("a href=")[1].split()[0])
        count += 1
    page = page + 1
    url = 'https://www.104.com.tw/jobbank/joblist/joblist.cfm?jobsource=104_bank1&ro=0\
           &area=6001001000&indcat=1001001002&order=2&asc=0&page=' + str(page) + '&psl=N_A'
    time.sleep(5)
