import requests
import math
import time
from bs4 import BeautifulSoup
import lxml
import threading

def job_info(href):
    try:
        time.sleep(3)

        res = requests.get(href)
        soup = BeautifulSoup(res.text, "html5lib")  # Error lxml, html.parser
        # print(soup)

        if soup.select('head > title') != "104人力銀行─錯誤頁":

            job_company = soup.select('a')[1].text
            job_content = soup.select('div[class="content"] > p')[0].text  # 工作內容

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

            print("公司名稱\n" + job_company)
            print("--" * 30)
            print("工作內容\n" + job_content)
            print("--" * 30)
            print("擅長工具\n" + job_tools)
            print("--" * 30)
            print("工作技能\n" + job_skills)
            print("--" * 30)
            print("其他條件\n" + other_con)

            # new_info = job_tools + "," + job_skills + "," + other_cons
            #
            # for char in ['\n', '\r', '、', '，']:
            #     if char in new_info:
            #         new_info = new_info.replace(char, ' ')
            #
            # new_info = new_info.encode('ascii', 'ignore').decode('utf8')
            # print(new_info)

        else:
            print("404 Not Found")

    except IndexError as e:
        print(e, href)

    except:
        print("Other Exception: " + href)

job_info("https://www.104.com.tw/job/?jobno=5ezog&jobsource=104_hotorder")

