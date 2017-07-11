# After Crawler104.py

# 從存入job104p1, p2或p3的網址去爬104的職缺網頁內文
# 然後取出所有非ASCII的字串

# 跑之前請先將準備好的job104p1,p2或p3.sqlite放在目前的資料夾中
# 並依需求更改p1為p2或p3
# 改完之後即可將步驟1~5全跑一次


# 步驟1
from bs4 import BeautifulSoup
import requests
import bs4
import time
import re
import sqlite3
import pprint

# 步驟2
# 定義 job104_for_info 方法
# 參數href為要爬的網頁的網址
# 爬網頁之後解析出內文並回存進資料庫
# (假設所需的套件都已經啟用)

# 請依需求更改p1為p2或p3

def job104_for_info(href): 

    try:

        time.sleep(2)
        
        # 爬進資料
        # 用lxml會出現錯誤,得用Python預設的html.parser
        
        res = requests.get(href)
        soup = BeautifulSoup(res.text,'html.parser')
        
        if soup.select('head > title') != "104人力銀行─錯誤頁":    # 跳過過期的職缺頁面

            # 拆解資料

            # 工作內容 (job_desc)

            job_desc = soup.select('div[class="content"] > p')[0].text

            # 擅長工具 (job_tools)
            # 工作技能 (job_skills)
            # 其他條件 (other_cons)

            reqs = soup.find_all(["dt","dd"])

            job_tools = ""
            job_skills = ""
            other_cons = ""

            for i in range(0,len(reqs)-1):
                if "擅長工具" in reqs[i].text:
                    job_tools += reqs[i+1].text
                elif "工作技能" in reqs[i].text:
                    job_skills += reqs[i+1].text
                elif "其他條件" in reqs[i].text:
                    other_cons += reqs[i+1].text

            # 將找到的資料都串起來        

            new_info = job_desc + "," + job_tools + "," + job_skills + "," + other_cons

            for char in ['\n','\r','、','，']:
                if char in new_info:
                    new_info = new_info.replace(char,' ')

            new_info = new_info.encode('ascii','ignore').decode('utf8')
            # print(new_info)

            # 將資料上傳到資料庫裡

#            with sqlite3.connect('job104p1.sqlite') as conn:
            with sqlite3.connect('job104p2.sqlite') as conn:
#             with sqlite3.connect('job104p3.sqlite') as conn:
                c = conn.cursor()
                save_info = "update job104 set info = ? where href = ?;" 
                c.execute(save_info,(new_info,href))
        
        else:
            print("404網頁不存在")
    
    #如果網頁異常則拋出例外
    
    except IndexError as e:
        print(e, href)

    except:
        print("其他例外: " + href)
        
#爬蟲例外 例外方法寫在def裏面
        
class CrawlerError(Exception): 
    pass


# 步驟3
# 定義update_None_info方法
# 從資料庫找出需要抓的網頁的網址
# 然後一筆一筆抓
# 存進資料庫

# 請依需求更改p1為p2或p3

def update_None_info(): 
       
#     from bs4 import BeautifulSoup
#     import requests
#     import bs4
#     import time
#     import re
#     import sqlite3
    
    try:
#        with sqlite3.connect('job104p1.sqlite') as conn:
        with sqlite3.connect('job104p2.sqlite') as conn:
#         with sqlite3.connect('job104p3.sqlite') as conn:

            c = conn.cursor()
            
            # 找出info是空的url並找出網址list
            
            qryString = "SELECT href FROM job104 where info is '';" 
            c.execute(qryString)
            
            # 計算有多少筆完成
            
            do_number = 0 
            lst = c.fetchall()
            
            # 控制爬網最大比數
            
#             lst[0:1000]    
            
            #跑迴圈執行
            
            for a in lst:
                if "hunter.104.com.tw" not in a[0]: #開頭網址不是獵頭網的才進入迴圈
                    job104_for_info(a[0]) 
#                     print(a[0])
                    do_number +=1
                    print(do_number)

                else:
                    print("獵頭網頁") #若出現則顯示外包網頁
                              
            print('Has crawled {} info!'.format(do_number))
                        
    except ConnectionError as e:
        print(e)
        print(a)
        print(href)
        
    except CrawlerError as e:
        print(a)
        print(e)
    finally:
        conn.close()


# 步驟3
# 執行update_None_info方法

update_None_info()


# 步驟4
# 檢視存進資料庫的資料

# 請依需求更改p1為p2或p3

#with sqlite3.connect('job104p1.sqlite') as conn: 
with sqlite3.connect('job104p2.sqlite') as conn: 
# with sqlite3.connect('job104p3.sqlite') as conn: 
    c = conn.cursor()
    pprint.pprint(list(c.execute('select * from job104 limit 0, 20;')))
#     pprint.pprint(list(c.execute('select count(*) from job104 where info != "";')))
conn.close()



# 加入單筆
# jid = 1

# with sqlite3.connect('job.sqlite') as conn:
#     c = conn.cursor()
# #     c.execute('select * from job518')
# #     print(c.fetchone())
#     updStrting = 'update job518 set info =:info where jobID =:jobID'
#     c.execute(updStrting, {'info' : new_info, 'jobID' : jid})

# with sqlite3.connect('job.sqlite') as conn:
#     c = conn.cursor()
#     c.execute('select * from job518')
#     print(c.fetchone())