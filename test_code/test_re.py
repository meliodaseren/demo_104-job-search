import re

str = "https://www.104.com.twhttp://hunter.104.com.tw/104hunter.jsp?trc=104p&jobsource=n104bank1&urlpage=job_description&jobno=9321344"

# 編譯成 Pattern 對象
pattern = re.compile(r'https://www.104.com.twhttp://hunter.104.com.tw/.+')

# 取得匹配結果，無法匹配返回 None
match = pattern.match(str)

if match:
    # 得到匹配結果
    print(match.group())