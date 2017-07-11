
import requests
from bs4 import BeautifulSoup as bs
import lxml
import html5lib
import re
res=requests.get("http://coolpc.com.tw/evaluate.php")
soup=bs(res.text,'html5lib')
cpu=soup.select("#tbdy > tr")[3].select("optgroup > option")
data=[row.text for row in cpu] # data=dict 裡面有row.text 在CPU
result_cpu=[]
for row in data:
    cpu={}
    cpu['brand']=row.split(' ')[0]
    cpu['name']=row.split('/')[0]
    cpu['catch']=row.split('/')[1]
    power=re.findall('(\d+W)',row)
    cpu['耗電量']=power[0] if power else ""
    price=re.findall('\$(\d+)',row)
    cpu['price']=int(price[0]) if price else 0
    Gz = re.findall('(\d.\d)(GHZ|GHz|G)',row)[0]
    per_price=int(price[0])/float(Gz[0])
    cpu['perGHz']='{:.2f}'.format(per_price)
    kernel=re.findall('【\w*】',row)[0]
    if kernel == '【雙核】':
         cpu['kernel']=2
    elif kernel == '【四核】':
        cpu['kernel']=4
    elif kernel == '【六核】':
        cpu['kernel']=6
    elif kernel == '【八核】':
        cpu['kernel']=8
    elif kernel == '【十核】':
        cpu['kernel']=10
    elif kernel == '【十二核】':
        cpu['kernel']=12
    else:
        cpu['kernel']=14
    result_cpu.append(cpu)
result_cpu