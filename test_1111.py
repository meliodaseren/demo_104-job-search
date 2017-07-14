import requests
from bs4 import BeautifulSoup as bs4
import time
import lxml

try:
    for i in range(1, 151):
        set1 = set()
        url = "https://www.1111.com.tw/job-bank/job-index.asp?si=1&ss=s&ks=%E8%B3%87%E6%96%99%E5%88%86%E6%9E%90&page=" + str(
            i)
        re=requests.get(url,"https:111.242.191.115:53281")
        soup = bs4(re.text, 'lxml')
        # print(soup.select(".jbInfoin > h3 > a "))
        for murl in soup.select(".jbInfoin > h3 > a"):
            # nu=str(murl["href"]).split("/")[1].split("&")[0]
            nu = str(murl["href"].split('/')[4])
            set1.add(nu)
        # print(set1)
        for surl in set1:
            url1 = "https://www.1111.com.tw/job/" + str(surl)+"/"
            re1 = requests.get(url1,"http://59.126.48.8:8080")
            #print(re1.text)
            soup = bs4(re1.text, 'lxml')
            s1 = soup.findAll("div",attrs={"class":"listContent"})[12]
            print(s1)
            print("=="*50)
            for title in soup.select(".logoTitle > h1"):
                print(title.text)
                for tool in soup.findAll("div"):
                    print(str(tool).split('電腦專長')[1])
        time.sleep(5)
except:
    pass