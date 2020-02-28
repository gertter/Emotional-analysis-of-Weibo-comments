#-*- coding: utf-8 -*-
from urllib.parse import urlencode
import requests
import json
import re
import sys
from bs4 import BeautifulSoup
nums =1
list = []
l=False
keys = 0
import os

def get_req(url):
    response = requests.get(url)
    import time
    time.sleep(1)
    response.encoding='utf-8'
    if response.status_code == 200:
        return response.text
    else:
        return None
def get_since_id(text):
    all_json_text = json.loads(text)
    since_id = all_json_text["data"]['cardlistInfo']['since_id']
    return since_id
def get_write(text):
    with open("info.txt","a+") as f:
        f.write(str(text)+'\n')
        f.close()
def get_page_url(text):
    global l
    if text==None:
        pass
    else:
        all_json_text=json.loads(text)
        text_url_list=all_json_text["data"]['cards']
        list=[]
        keys=0
        for i in range(len(text_url_list)):
            if 'scheme' in text_url_list[i]:
                title = re.sub('[A-Za-z0-9\!\%\[\]\,\。</></>=\&\-"\?\.:\+“”#;【____ \s'']', "",
                               text_url_list[i]['mblog']['text'])
                pub_time = text_url_list[i]['mblog']['created_at']
                if '02-24' in pub_time:
                    l=True
                if '01-23' in pub_time:
                    return 'Over'
                if l==True:
                    print(pub_time,title)
                    if '疫' in title or '确诊' in title or '病例' in title:
                        data = {
                            'i_key': keys,
                            'url': text_url_list[i]['scheme'],
                            'pub_time': pub_time,
                            'id': text_url_list[i]['mblog']['id'],
                            'title': title,
                        }
                        keys += 1
                        get_write(data)
                        list.append(data)
            else:
                continue
        return list
def main(url):
    global nums
    all_text=get_req(url)
    title_list=get_page_url(all_text)
    if title_list=='Over':
        sys.exit(0)
    if len(title_list)==0:
        since_id = get_since_id(all_text)
        next_url = get__title_next_url(since_id)
        main(next_url)
    else:
        since_id = get_since_id(all_text)
        next_url = get__title_next_url(since_id)
        main(next_url)
def get__title_next_url(since_id):
    url='https://m.weibo.cn/api/container/getIndex?'
    data = {
        'type': 'uid',
        'value': '2803301701',
        'containerid': '1076032803301701',
        'since_id':str(since_id),
    }
    return url+urlencode(data)

def get_req_comment(url,per):
    header = {
        'Cookie': 'cookie: _T_WM=98973286548; ALF=1584795013; SCF=ApjS4K1Th1NowPnw0wn82r3DZYNXa0TMwe0pJ32ikoUV3_XI_5_oaopDZiyvdYfws1D5O18QLOLVTKY_A9ig1L8.; SUB=_2A25zSvDYDeRhGeFN4lQR9i_IwzSIHXVQtJCQrDV6PUJbktAKLXb4kW1NQ6UbuFv3z1OtjW5U8p866yixbIMmMaDn; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9Wh1TjQIJIYwnvEGa-9_D2x35JpX5KzhUgL.FoM01Kq7So2X1hn2dJLoIp7LxKML1KBLBKnLxKqL1hnLBoMEeo5E1hMpeoM7; SUHB=09P9_OCzX9wMmP; MLOGIN=1; WEIBOCN_FROM=1110006030; XSRF-TOKEN=f9a4d0; M_WEIBOCN_PARAMS=oid%3D4468631603408517%26luicode%3D20000061%26lfid%3D4468631603408517%26uicode%3D20000061%26fid%3D4468631603408517',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3970.5 Safari/537.36',
        'referer': per,
    }
    response = requests.get(url,headers=header)
    import time
    time.sleep(1)
    response.encoding = 'utf-8'
    if response.status_code == 200:
        return response.text
    else:
        return None
if __name__=='__main__':
    print("*********这里是人名日报微博情绪系统**************")
    print("加载中,请等待...")
    data = {
        'type': 'uid',
        'value': '2803301701',
        'containerid': '1076032803301701'
    }
    url = 'https://m.weibo.cn/api/container/getIndex?' + urlencode(data)
    main(url)

