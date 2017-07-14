from bs4 import BeautifulSoup
import requests

res = requests.get('https://www.104.com.tw/job/?jobno=5ezog&amp;jobsource=104_hotorder')
soup = BeautifulSoup(res.text, 'lxml')

# keyword = ['公司福利', '工程師']
# level =['專科', '大學', '碩士']
# lang = ['不拘', 'linux', 'java', 'javascript', 'mysql', 'ms sql', 'android', 'jsp',\
#         'ios app', 'c', 'c++', 'python', 'ruby', 'scala', 'hadoop', 'spark'] + level + keyword

lang = ['不拘', 'linux', 'java', 'javascript', 'mysql', 'ms sql', 'android', 'jsp',\
        'ios app', 'c', 'c++', 'python', 'ruby', 'scala', 'hadoop', 'spark']

tmp = soup.findAll('title')
print(tmp)
lib = []
for tmp in soup.find_all('section'):
    tmp2 = "".join(tmp.text.lower().strip())
    for ti in lang:
        if tmp2.find(ti) >= 0:
            if tmp2 not in lib:
                # lib.append(tmp2)
                print(ti.title())
                # print(''.join(tmp2.split(':')))

# for tmp in soup.find_all('dd'):
#     tmp2 = "".join(tmp.text.lower().strip().split())
#     for xx in lang:
#         if tmp2.find(xx) >= 0:
#             print(tmp2)