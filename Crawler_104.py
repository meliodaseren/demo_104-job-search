import requests
import math
import time
from bs4 import BeautifulSoup
import lxml
import threading
import json

# index page [test: 資訊軟體系統類]
# index = "https://www.104.com.tw/jobbank/joblist/joblist.cfm?jobsource=n104bank1&ro=0&jobcat=2007000000&order=2&asc=0&page=1"

# index page [test: BIOS工程師、本日最新 2017/7/14 19:08 共 13 筆]
index = "https://www.104.com.tw/jobbank/joblist/joblist.cfm?jobsource=n104bank1&ro=1&jobcat=2007001011&isnew=0&order=2&asc=0&page=1"

# href selector
# soup.select('div.jobname_summary')[0].select('a')[0]['href']


print("==" * 25)

# The function to get title of page lists
def getListsTitle(href):
    res = requests.get(href)
    # get index job lists title
    indexTitle = BeautifulSoup(res.text, 'lxml').select('div[class="cond_lists"]')[0].select('a')[0].text

    res.close()
    return indexTitle

pageTitle = getListsTitle(index)
print('Page Lists Title: ' + pageTitle)


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

totalPages = getTotalPage(index)
print('Total Pages: ' + str(totalPages))

print("==" * 25)


# create dictionary to export json
job_lists_dict = {
    "lists_url": index,
    "total_pages": totalPages,
    "lists_title": pageTitle,
    "job_lists": []
}


# The function to get job information
def job_info(href):
    try:
        time.sleep(5)

        res = requests.get(href)
        soup = BeautifulSoup(res.text, "html5lib")  # Error lxml, html.parser
        # print(soup)

        if soup.select('head > title') != "104人力銀行─錯誤頁":

            job_company = soup.select('a')[1].text                         # json[3] company   公司名稱
            job_content = soup.select('div[class="content"] > p')[0].text  # json[4] content   工作內容
            job_uptime = soup.select('time[class="update"]')[0].text       # json[8] post_data 公布時間

            reqs = soup.find_all(["dt", "dd"])
            # print(reqs)
            job_tools = ""   # json[5] tools  擅長工具
            job_skills = ""  # json[6] skills 工作技能
            other_con = ""   # json[7] other  其他條件

            for i in range(0, len(reqs) - 1):
                if "擅長工具" in reqs[i].text:
                    job_tools += reqs[i + 1].text
                elif "工作技能" in reqs[i].text:
                    job_skills += reqs[i + 1].text
                elif "其他條件" in reqs[i].text:
                    other_con += reqs[i + 1].text

            job_info_dict = {
                "company": job_company,
                "content": job_content,
                "tools": job_tools,
                "skills": job_skills,
                "other": other_con,
                "post_date": job_uptime
            }

            return job_info_dict

            # check output
            # print("* 公司名稱：" + job_company)
            # print("* 工作內容\n" + job_content)
            # print("* 擅長工具：" + job_tools)
            # print("* 工作技能：" + job_skills)
            # print("* 其他條件\n" + other_con)
            # print("* " + job_uptime)

        else:
            print("404 Not Found")

    except IndexError as e:
        print(e, href)

    except:
        print("Other Exception: " + href)

    finally:
        pass


# Save each job page url
for page in range(1, totalPages + 1):
    indexf = index[:-1] + "{}"
    href = indexf.format(page)
    soup = BeautifulSoup(requests.get(href).text, 'lxml')
    jobnameSoup = soup.select('div.job_name')
    totalJobname = len(jobnameSoup)

    if page % 10 == 0:
        print('Progress: ' + str(page) + ' / ' + str(totalPages) + ' pages')

    count = 0

    for jn in range(0, totalJobname):
        title = soup.select('div.job_name')[jn].text.strip()
        href = "https://www.104.com.tw" + jobnameSoup[jn].select('a')[0]['href']

        job_dict = {
            "title": title,
            "url": href
        }

        # check output
        # print(title)  # json[1] title 職稱
        # print(href)   # json[2] url   工作頁面連結
        # print("--" * 50)
        # print(job_dict)
        # print(job_info(href))
        # print("--" * 50)

        # update dictionary
        job_dict.update(job_info(href))
        # print(job_dict)
        # print("--" * 50)

        # append dictionary to list
        job_lists_dict["job_lists"].append(job_dict)
        # print(job_lists_dict["job_lists"])

        count += 1
        print(count)

    time.sleep(5)

print(job_lists_dict)

print(str(totalPages) + 'Done.')
