from bs4 import BeautifulSoup as bs
import requests

res = requests.get("https://www.104.com.tw/job/?jobno=4twky&jobsource=104_hotorder")
soup = bs(res.text,"lxml")
keyword = ['公司福利','工程師']
level =['專科','大學''碩士']
lang = ['linux','java','javascript','mysql',"ms sql",'不拘','android','jsp', 'ios app']+level+keyword
tmp = soup.findAll('title')
print(tmp)
lib = []
for tmp in soup.find_all('section'):
    tmp2 = "".join(tmp.text.lower().strip())
    for xx in lang:
        if tmp2.find(xx) >= 0:
            if tmp2 not in lib:
                # lib.append(tmp2)
                print('>> ' + xx.title() + ' <<')
                # print(''.join(tmp2.split(':')))

# for tmp in soup.find_all('dd'):
#     tmp2 = "".join(tmp.text.lower().strip().split())
#     for xx in lang:
#         if tmp2.find(xx) >= 0:
#             print(tmp2)