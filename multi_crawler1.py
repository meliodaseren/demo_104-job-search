import time
import threading

class myThread (threading.Thread):
   def __init__(self, threadID, name,initurl,delay,proxy,dest):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.initurl=initurl
      self.delay=delay
      self.proxy=proxy
      self.dest=dest


   def run (self):
       crawyer104(self.initurl,self.delay,self.proxy,self.dest)

class myThread1 (threading.Thread):
   def __init__(self, threadID, name,initurl,delay,proxy,dest):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.initurl=initurl
      self.delay=delay
      self.proxy=proxy
      self.dest=dest


   def run (self):
       crawler1111(self.initurl,self.delay,self.proxy,self.dest)

def crawyer104 (initurl,delay,proxy,dest_path):
    import requests
    from bs4 import BeautifulSoup
    import lxml
    from collections import Counter
    import time
    import json
    cnt={}#比較器
    count=1      #偵錯用
    try:
        #p=1 #第一頁
        for i in range(1,150):
            set1=set()
            url=initurl+str(i)+"&psl=N_A"
            re =requests.get(url,proxy)
            soup=BeautifulSoup(re.text,'lxml')
            #print(soup.select(".job_name > a"))
            # next=soup.select(".mar_L10 ")[0]
            # print(next.text)
            for murl in soup.select(".job_name > a"):
                nu=str(murl["href"]).split("jobno=")[1].split("&")[0]
                set1.add(nu)
            for surl in set1:
                url1="http://www.104.com.tw//job/?jobno="+str(surl)+"&amp;jobsource=n104bank1&amp;hotjob_chr="
                re1=requests.get(url1)
                soup=BeautifulSoup(re1.text,'lxml')
                print("第%d筆更新" %(count))
                for title in soup.select('title'):
                    print(str(title).split('<title>')[1].split('-')[0])
                    print("="*50)
                    print("擅長工具:")
                    count+=1
                    tc=0
                    for tool in soup.select(".tool > a"):
                        tc+=1
                        print(tool.text)
                        if tool.text in cnt:
                            cnt[tool.text]+=1
                        else:
                            cnt[tool.text]=1
                    if tc < 1:
                    	    print("不拘")
                    	    #cnt["不拘"]+=1
               	    print("=" * 50)
            time.sleep(delay)
        # print(type(cnt.most_common(20)))
        for key in cnt:
            print("{}   有{}個工作要求".format(key,cnt.get(key)))
        # print(cnt)
        # with open("dest.txt", "a", encoding="utf-8") as f:
        #     f.write("{} \n".format(myThread.name))
        # for key in cnt:
        #     print("{}   有{}個工作要求".format(key,cnt.get(key)))
        #     with open(dest_path,"a",encoding="utf-8") as f:
        #         f.write("{}   有{}個工作要求\n".format(key,cnt.get(key)))
        # with open(dest_path, "a", encoding="utf-8") as f:
        #     f.write("前20名的被工作要求的語言:")
        # with open(dest_path,"a",encoding="utf-8") as f:
        #     f.write("{}".format(cnt.most_common(20)))
        # js=json.dumps(cnt,sort_keys=True,ensure_ascii=False)
        # print(type(js))
        with open(dest_path,'a',encoding="utf-8") as f:
            f.write(json.dumps(cnt,sort_keys=True,ensure_ascii=False))
            f.close()

    except requests.ConnectionError:
            print("Connection aborted")

def crawler1111(initurl,delay,proxy,dest_path):
    import requests
    from bs4 import BeautifulSoup as bs4
    import time
    import lxml
    dict1 = {}
    list1 = []
    count = 1
    try:
        for i in range(1, 151):
            set1 = set()
            url = initurl + str(i)
            re = requests.get(url,proxy)
            soup = bs4(re.text, 'lxml')
            # print(soup.select(".jbInfoin > h3 > a "))
            for murl in soup.select(".jbInfoin > h3 > a"):
                # nu=str(murl["href"]).split("/")[1].split("&")[0]
                nu = str(murl["href"].split('/')[4])
                set1.add(nu)
            # print(set1)
            for surl in set1:
                url1 = "https://www.1111.com.tw/job/" + str(surl) + "/"
                re1 = requests.get(url1, "http://59.126.48.8:8080")
                # print(re1.text)
                soup = bs4(re1.text, 'lxml')
                # s1 = soup.findAll("div",attrs={"class":"listContent"})[12]
                # print(s1)
                # print("=="*50)
                for title in soup.select(".logoTitle > h1"):
                    sumtitle = title.text
                    # dict1.setdefault(sumtitle)
                    print("第%d筆更新" % count)
                    print(sumtitle)
                    count+=1
                    for tool in soup.findAll("div", {"class": "floatL w65"}):
                        a = (tool.text).replace("  ", "").split("要求條件")[1].split("應徵方式")[0].replace("\n", "").replace(
                            ":", "=")
                        list1.append(a)
                        dict1[sumtitle] = list1
                        print(a)
                        print("==" * 50)
            time.sleep(delay)
        print(type(dict1))
        with open(dest_path,"a",encoding="utf-8") as f:
            f.write(str(dict1))
            f.close()


    except:
        pass



if __name__ == '__main__':
    url = "https://www.104.com.tw/jobbank/joblist/joblist.cfm?jobsource=n104bank1&ro=0&keyword=%E8%BB%9F%E9%AB%94%E5%B7%A5%E7%A8%8B%E5%B8%AB&order=1&asc=0&page="
    url1 = "https://www.1111.com.tw/job-bank/job-index.asp?si=1&ks=%E8%BB%9F%E9%AB%94%E5%B7%A5%E7%A8%8B%E5%B8%AB&fs=1&page="
    dest="crawler_1.txt"
    dest1="crawler_2.txt"
    thread1=myThread(1,"104",url,3,"https://125.224.233.167:3128",dest)
    thread2=myThread1(2,"1111",url1,2,"https:111.242.191.115:53281",dest1)
    threads=[]

    try:
        thread1.start()
        thread2.start()
        # with open(dest,'a',encoding="utf-8") as f :
        #     f.write(thread1.name+"\n")
        #     f.close()
        # with open(dest1,'a',encoding="utf-8") as f :
        #     f.write(thread2.name+"\n")
        #     f.close()
        threads.append(thread1)
        threads.append(thread2)
        for t in threads:
            t.join()
            print(" {} Exiting Main Thread".format(t))
    except:
        pass

