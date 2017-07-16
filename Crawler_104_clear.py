import requests
import math
import time
from bs4 import BeautifulSoup
import lxml
import threading
import re
import json

# ----- Crawler Information ----- #

# index page
# [資訊軟體系統類]  jobcat=2007000000
# [軟體╱工程類人員] jobcat=2007001001 - 2007001012
# [MIS╱網管類人員] jobcat=2007002001 - 2007002008
jobcat = 1002
index = "https://www.104.com.tw/jobbank/joblist/joblist.cfm?jobsource=n104bank1&ro=0&jobcat=200700{}&order=2&asc=0&page=1".format(jobcat)

# ------------------------------- #

print("--" * 25)

# The function to get title of page lists
def getListsTitle(href):
    res = requests.get(href)
    # get index job lists title
    indexTitle = BeautifulSoup(res.text, "lxml").select('div[class="cond_lists"]')[0].select('a')[0].text

    res.close()
    return indexTitle

pageTitle = getListsTitle(index)
print("Page Lists Title: " + pageTitle)


# The function to get total pages
def getTotalPage(href):
    res = requests.get(href)
    totalPages = int(BeautifulSoup(res.text, "lxml").select('form#jobform')[0].select('ul')[0]
                                                    .select('li')[0].text.split("筆")[0][1:].strip())
    res.close()
    # 20 job urls in each page, but only get page 150
    totalPages = 150 if math.ceil(totalPages / 20) > 150 else math.ceil(totalPages / 20)
    return totalPages

totalPages = getTotalPage(index)
print("Total Pages: " + str(totalPages))

print("--" * 25)


# create dictionary to export JSON
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

        if soup.select('head > title') != "104人力銀行─錯誤頁":
            job_company = soup.select('a')[1].text
            job_content = soup.select('div[class="content"] > p')[0].text
            job_uptime = soup.select('time[class="update"]')[0].text

            reqs = soup.find_all(['dt', 'dd'])
            job_tools = ""
            job_skills = ""
            other_con = ""

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
                "post_date": job_uptime,
                "other_condition": other_con
            }

            return job_info_dict

        else:
            print("404 Not Found")

    except IndexError as e:
        print(e, href)

    except:
        print("Other Exception: " + href)

    finally:
        pass


# Save each job page url
try:
    for page in range(1, totalPages + 1):
        indexf = index[:-1] + "{}"
        href = indexf.format(page)
        soup = BeautifulSoup(requests.get(href).text, "lxml")

        jobnameSoup = soup.select('div.job_name')
        totalJobname = len(jobnameSoup)

        count = 0

        for jobName in range(0, totalJobname):
            title = soup.select('div.job_name')[jobName].text.strip()
            href = "https://www.104.com.tw" + jobnameSoup[jobName].select('a')[0]['href']

            # -------------------------------------------------------------------------- #
            # Bad ! Need Fixed !
            # Fixed exception: 'NoneType' object is not iterable
            # Hint: https://www.104.com.tw/job/
            pattern = re.compile(r'https://www.104.com.twhttp://hunter.104.com.tw/.+')
            match = pattern.match(href)
            pattern2 = re.compile(r'https://www.104.com.twhttp://tutor.104.com.tw/.+')
            match2 = pattern2.match(href)
            if match:
                continue  # hunter.104.com.tw
            elif match2:
                continue  # tutor.104.com.tw
            elif href == "https://www.104.com.twjavascript:void(0)":
                continue  # case.104.com.tw
            # -------------------------------------------------------------------------- #

            job_dict = {
                "title": title,
                "url": href
            }

            # update dictionary
            job_dict.update(job_info(href))

            # append dictionary to list
            job_lists_dict["job_lists"].append(job_dict)

            count += 1
            print("Scraping: " + str(count) + " (" + str(page) + " / " + str(totalPages) + " Pages)")

        time.sleep(5)
finally:
    pass


# Writing JSON data
def saveJson(data, fileName):
    with open(fileName, "w", encoding="utf8") as f:
        json.dump(data, f, ensure_ascii=False)

saveJson(job_lists_dict, "Job_104_" + str(jobcat) + ".json")


print(str(totalPages) + " Pages Done.")
