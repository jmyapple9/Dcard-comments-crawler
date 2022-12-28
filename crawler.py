import urllib.request as req
from bs4 import BeautifulSoup
import re
import json
import numpy as np
import contextlib
import time
import random
def variables_setup():
    # url=input('url:')
    global url,U,comment,schoolname,gender,user_agents,proxy_list
    url="https://www.dcard.tw/f/mood/p/240862682"
    U=url[-9:]
    comment=[]
    schoolname=[]
    gender=[]
    user_agents=[
        
        'Opera/9.25 (Windows NT 5.1; U; en)',
        'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',
        'Roku/DVP-9.10 (519.10E04111A)',
        'Netscape/13.4 (BeOS 3.6; ar_DZ;)',
        'Maxthon/11.20 (BeOS 3.5; ar_BH;)',
        'CriOS/10.9 (BeOS 3.5; ar_YE;)',
        'Flock/3.8 (BeOS 4.8; ar_BH;)',
        'Flock/10.20 (BeOS 3.1; de_AT;)',
        'Safari/3.20 (BeOS 1.9; en;)',
        'Mozilla/4.41 (BEOS; U ;Nav)',
        'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
        'Tumbleweed 0.1 BeOS',
        
    ]
    proxy_list = [
        '163.204.246.249:9999',
        '163.204.240.222:9999',
        '114.100.2.79:9999',
        '110.243.23.125:9999',
        '163.204.244.30:9999',
        '61.161.27.155:9999',
        '60.174.191.11:9999'
        # '183.95.80.102:8080',
        # '123.160.31.71:8080',
        # '115.231.128.79:8080',
        # '166.111.77.32:80',
        # '43.240.138.31:8080',
        # '218.201.98.196:3128'
    ]

def parseJson(n):
    # proxy = random.choice(proxy_list)
    # urlhandle = req.ProxyHandler({'http': proxy})
    # opener = req.build_opener(urlhandle)
    # req.install_opener(opener)

    R=req.Request(f"https://www.dcard.tw/service/api/v2/posts/{U}/comments?after={n-3}",headers={
        "user-agent":user_agents[(n//400)%12]

    })
    # time.sleep(0.4)
    
    print(f'loading...{(n//400)%12}')
    with req.urlopen(R) as response:
        data = response.read().decode("utf-8")
    WW=BeautifulSoup(data,"html.parser")
    Wjson=json.loads(WW.text)
    if Wjson==[]:
        return
    for ww in Wjson:
        comment.append(ww.get('content') if ww.get('content') else "Deleted")
        schoolname.append(ww.get('school') if ww.get('school') else "Deleted")
        gender.append(('男' if ww.get('gender')=='M' else '女') if ww.get('gender') else "unknown")
    
    parseJson(n+30)

if __name__ == '__main__':
    variables_setup()
    # proxy = random.choice(proxy_list)
    # urlhandle = req.ProxyHandler({'http': proxy})
    # opener = req.build_opener(urlhandle)
    # req.install_opener(opener)
    # print(proxy)
    request=req.Request(url,headers={
        "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        # "user-agent":'Maxthon/11.20 (BeOS 3.5; ar_BH;)'
        # "path":"/service/api/v2/posts/236469753/comments?after=50",
        # "method": "GET",
        # "referer": "https://www.dcard.tw/f/funny/p/236469753",
    })
    with contextlib.closing(req.urlopen(request)) as response:
        data=response.read().decode("utf-8")

    root=BeautifulSoup(data,"html.parser")
    # css_root=BeautifulSoup('<div style="padding-top: 0px; padding-bottom: 5703.73px;">', "html.parser")
    # for i in range(10,20):
    # arr=np.zeros(100, dtype=type(root.select(f'div[data-index="0"]')))
    for i in range(80):
        if i==53:
            parseJson(i)
            break

        target=root.select(f'div[data-index="{i}"]')
        school=BeautifulSoup(str(target),"html.parser").find_all("div",class_="sc-7fxob4-4 dbFiwE") #find school
        if str(school) !="[]":
            for sch in school:
                tmp=sch.string
            schoolname.append(tmp)
        
        Tmp=''
        tmp_gen="Unknown"
        for item in target:
            # T=item.select("span")
            A=item.find_all("div",class_="phqjxq-0 fQNVmg")
            G=item.find_all("title")
            for g in G:
                if g is not None:
                    tmp_gen=g.string
            for a in A:
                if a is not None:
                    Tmp=a.getText() if a.getText() else "No text"
                    # Tmp=Tmp+a.getText()+t.getText()+'\n'
        
        if Tmp !='':
            gender.append(tmp_gen)
            comment.append(Tmp)
            # print(f'{1+i},{tmp_gen},{Tmp}')
        
        
    count=1
    # searchList = ['臺灣大學', '清華','交通','成功','政治']
    List=['密碼','B']

    for sch,com,gen in zip(schoolname,comment,gender):
        if any(x in com for x in List):
            print(f'B{count}:{gen}---------------------------{sch}---------------------------\n{com}\n')
        # print(f'B{count}:{gen}---------------------------{sch}---------------------------\n{com}\n')
        count+=1

    # tar=root.find_all("div",string=re.compile("大學$")) #find school
    # for item in tar:
    #     print(item.string)

    # tag=css_root.find_all("div",style="padding-top: 0px; padding-bottom: 5703.73px;")
    # print(item.div)
