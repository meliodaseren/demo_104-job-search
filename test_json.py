# https://docs.python.org/3/library/json.html

import json

data = {
    'name': 'ACME',
    'shares': 100,
    'price': 542.23
}

# python data -> json
json_str = json.dumps(data)
print(json_str)
print(type(json_str))

# json -> python data
data2 = json.loads(json_str)
print(data2)
print(type(data2))




# json[1] title     職稱
# json[2] url       工作頁面連結
# json[3] company   公司名稱
# json[4] content   工作內容
# json[5] tools     擅長工具
# json[6] skills    工作技能
# json[7] other     其他條件
# json[8] post_data 公布時間

""" 預計輸出格式
{
    "lists_url": "https://www.104.com.tw/jobbank/joblist/joblist.cfm?jobsource=n104bank1&ro=0&jobcat=2007000000&order=2&asc=0&page=1"
    "total_pages": 150
    "lists_title": "資訊軟體系統類"
    "job_lists": [
        {
            "title": "App Store /Android 手機技術人員(月領3萬至8萬,獎金另計)"
            "url": "https://www.104.com.tw/job/?jobno=5ezog&jobsource=104_hotorder"
            "company": "樂盈資訊國際有限公司"
            "content": "1.配合其他開發人員、測試人員，完成產品設計和發佈
                        2.持續學習新技術並導入產品開發 
                        3.編寫相關開發文檔、技術資料等 
                        4.手機網頁/介面優化 
                        5. App Store /Android 上架"
            "tools": "Android、iOS、Objective-C、JavaScript"
            "skills": "不拘"
            "other": "1.擅溝通協調，積極進取、工作配合度及抗壓性高。 
                      2.熟悉 JSON API 的串接 
                      3.精通 Android Studio, XCode 
                      4.需有 Android/IOS 上架經驗為佳"
            "post_date": "2017-07-12"
        },
        {
            "title":
            "url":
            "company":
            "content":
            "tools":
            "skills":
            "other":
            "post_date":
        },
        ...
    ]
}
"""

print("--" * 50)

# update()

job_dict = {'title': 'App Store /Android 手機技術人員(月領3萬至8萬,獎金另計)', 'url': 'https://www.104.com.tw/job/?jobno=5ezog&jobsource=104_hotorder'}

job_info = {'company': '樂盈資訊國際有限公司',
            'content': '1.配合其他開發人員、測試人員，完成產品設計和發佈 \n2.持續學習新技術並導入產品開發 \n3.編寫相關開發文檔、技術資料等 \n4.手機網頁/介面優化 \n5. App Store /Android 上架',
            'tools': 'Android、iOS、Objective-C、JavaScript',
            'skills': '不拘',
            'other': '1.擅溝通協調，積極進取、工作配合度及抗壓性高。 \n2.熟悉 JSON API 的串接 \n3.精通 Android Studio, XCode \n4.需有 Android/IOS 上架經驗為佳',
            'post_date': '更新日期：2017-07-12'}

job_dict.update(job_info)

print(job_dict)



