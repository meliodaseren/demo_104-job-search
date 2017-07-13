import requests
import math
import time
from bs4 import BeautifulSoup
import lxml
import threading


# href selector
# soup.select('div.jobname_summary')[0].select('a')[0]['href']

# The function to get total pages
def getTotalPage(href):
    res = requests.get(href)
    # 2017/7/11 23:30 共 20275 筆
    totalPages = int(BeautifulSoup(res.text, 'lxml').select('form#jobform')[0].select('ul')[0]
                                                    .select('li')[0].text.split('筆')[0][1:].strip())
    res.close()
    # 20 job hrefs in each page, but only get page 150
    totalPages = 150 if math.ceil(totalPages / 20) > 150 else math.ceil(totalPages / 20)
    return totalPages


# The function to get job information
def job_info(href):
    try:
        time.sleep(5)

        res = requests.get(href)
        soup = BeautifulSoup(res.text, "html5lib")  # Error lxml, html.parser
        # print(soup)

        if soup.select('head > title') != "104人力銀行─錯誤頁":

            job_company = soup.select('a')[1].text  # 公司名稱
            job_content = soup.select('div[class="content"] > p')[0].text  # 工作內容
            job_uptime = soup.select('time[class="update"]')[0].text

            reqs = soup.find_all(["dt", "dd"])
            # print(reqs)
            job_tools = ""   # 擅長工具
            job_skills = ""  # 工作技能
            other_con = ""  # 其他條件

            for i in range(0, len(reqs) - 1):
                if "擅長工具" in reqs[i].text:
                    job_tools += reqs[i + 1].text
                elif "工作技能" in reqs[i].text:
                    job_skills += reqs[i + 1].text
                elif "其他條件" in reqs[i].text:
                    other_con += reqs[i + 1].text

            print("* 公司名稱：" + job_company)
            print("* 工作內容\n" + job_content)
            print("* 擅長工具：" + job_tools)
            print("* 工作技能：" + job_skills)
            print("* 其他條件\n" + other_con)
            print("* " + job_uptime)

        else:
            print("404 Not Found")

    except IndexError as e:
        print(e, href)

    except:
        print("Other Exception: " + href)


# 資訊軟體系統類
totalPages = getTotalPage('https://www.104.com.tw/jobbank/joblist/joblist.cfm?jobsource=n104bank1&ro=0&jobcat=2007000000&order=2&asc=0&page=1')
print('Total Pages: ' + str(totalPages))


# Save each job page url
for page in range(1, totalPages + 1):
    href = "https://www.104.com.tw/jobbank/joblist/joblist.cfm?jobsource=n104bank1&ro=0&jobcat=2007000000&order=2&asc=0&page={}".format(page)
    soup = BeautifulSoup(requests.get(href).text, 'lxml')
    jobnameSoup = soup.select('div.job_name')
    totalJobname = len(jobnameSoup)

    if page % 10 == 0:
        print('Progress: ' + str(page) + ' / ' + str(totalPages) + ' pages')

    for jn in range(0, totalJobname):
        title = soup.select('div.job_name')[jn].text.strip()
        href = "https://www.104.com.tw" + jobnameSoup[jn].select('a')[0]['href']
        print(title)
        print(href)
        job_info(href)
        print("--" * 50)

    time.sleep(5)

print(str(totalPages) + 'Done.')
