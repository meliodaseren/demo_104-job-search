import requests
import math
import time
from bs4 import BeautifulSoup
import lxml


index = "https://www.zhihu.com/topic/19559450/top-answers"

# use User-Agent
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"}
res = requests.get(index, headers = headers)
print(res.status_code)

soup = BeautifulSoup(res.text, "lxml")

print(soup)