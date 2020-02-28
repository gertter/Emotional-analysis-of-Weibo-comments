#-*- coding: utf-8 -*-
from urllib.parse import urlencode
import requests
import json
import re
from bs4 import BeautifulSoup
nums =1
list = []
keys = 0
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
def get_write_info(text):
    with open("comment_info.txt","a+") as f:
        f.write(str(text)+'\n')
        f.close()
def get_page_url(text):
    if text==None:
        pass
    else:
        all_json_text=json.loads(text)
        text_url_list=all_json_text["data"]['cards']
        list=[]
        keys=0
        for i in range(len(text_url_list)):
            if 'scheme' in text_url_list[i]:
                print(text_url_list[i]['mblog']['created_at'])
                title = re.sub('[A-Za-z0-9\!\%\[\]\,\。</></>=\&\-"\?\.:\+“”#;【____ \s'']', "",
                               text_url_list[i]['mblog']['text'])
                pub_time = text_url_list[i]['mblog']['created_at']
                if '01-' in pub_time:
                    if '疫' in title or '确诊' in title or '病例' in title:
                        data = {
                            'i_key': keys,
                            'url': text_url_list[i]['scheme'],
                            'pub_time': pub_time,
                            'id': text_url_list[i]['mblog']['id'],
                            'title': title,
                        }
                        print('序号'+str(keys),data['pub_time']+"  "+data['title'])
                        keys += 1
                        list.append(data)
            else:
                continue
        return list

def get_max_id(text):
    max_id=re.findall('"max_id":(.*?),', text, re.S)[-1]
    return max_id
def U_change_C(u_text):
    data = {
            'content':u_text,
            'result':'',
            'untoch':'Unicode转中文'
        }
    resposne=requests.post('http://tool.chinaz.com/tools/unicode.aspx',data)
    resposne.encoding='utf-8'
    soup=BeautifulSoup(resposne.text,'lxml')
    comment_list=soup.select("#result")
    for o in comment_list:
        comment_text=re.search(r'name="result">(.*?)</textarea>',str(o),re.S)
        commnet_info=re.sub(r'[A-Za-z0-9\!\%\[\]\,\。</></>=\&\-"\.:\n\+“”#;【____ \s''\?\\\�]', "",  comment_text.group(1))
        if len(commnet_info)<3:
            pass
        else:
            get_write_info(commnet_info)
            print(commnet_info)
def get__title_next_url(since_id):
    url='https://m.weibo.cn/api/container/getIndex?'
    data = {
        'type': 'uid',
        'value': '2803301701',
        'containerid': '1076032803301701',
        'since_id':str(since_id),
    }
    return url+urlencode(data)
def get_title(text):
    global list,keys
    all_json_text = json.loads(text)
    text_url_list = all_json_text["data"]['cards']
    for i in range(len(text_url_list)):
        if 'scheme' in text_url_list[i]:
            print(text_url_list[i]['mblog']['created_at'])
            title=re.sub('[A-Za-z0-9\!\%\[\]\,\。</></>=\&\-"\?\.:\+“”#;【____ \s'']', "",
                                text_url_list[i]['mblog']['text'])
            pub_time=text_url_list[i]['mblog']['created_at']
            print('疫' in title or '确诊' in title or '病例' in title and '01'in pub_time)
            if '疫' in title or '确诊' in title or '病例' in title and '01'in pub_time:
                data = {
                    'i_key': keys,
                    'url': text_url_list[i]['scheme'],
                    'pub_time': pub_time,
                    'id': text_url_list[i]['mblog']['id'],
                    'title': title,
                }
                # print('序号' + str(keys), data['pub_time'] + "  " + data['title'])
                keys += 1
                list.append(data)
        else:
            pass
    return list
def main(url):
    global nums
    all_text=get_req(url)
    title_list=get_page_url(all_text)
    since_id=get_since_id(all_text)
    next_url=get__title_next_url(since_id)
    main(next_url)
    # else:
    #     try:
    #         print(title_list[int(key)])
    #         get_write_info(title_list[int(key)]['title'])
    #         first_comment_url = get_frist_coment_url(title_list[int(key)]['id'])
    #         get_comment(title_list[int(key)]['id'], first_comment_url,title_list[int(key)]['url'])
    #     except Exception as e:
    #         print("输入有误",e)
def get_frist_coment_url(id):
    data = {
        'id': str(id),
        'mid': str(id),
        'max_id_type': '0',
    }
    url = 'https://m.weibo.cn/comments/hotflow?' + urlencode(data)
    return url
def get_next_comment_url(id,max_id):
    data = {
        'id': str(id),
        'mid': str(id),
        'max_id':str(max_id),
        'max_id_type': '0',
    }
    url = 'https://m.weibo.cn/comments/hotflow?' + urlencode(data)
    return url
def get_comment(id,url,per):
    all_text = get_req_comment(url, per)
    try:
        commet_text = re.findall('"text":(.*?),',all_text, re.S)
        commet_text_list = re.findall('"(.*?)"', str(commet_text), re.S)
        for comment in commet_text_list :
            U_change_C(comment)
        max_id = get_max_id(all_text)
        next_url = get_next_comment_url(id,max_id)
        get_comment(id,next_url,per)
    except:
        max_id = get_max_id(all_text)
        next_url = get_next_comment_url(id, max_id)
        get_comment(id, next_url, per)
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
    print("以上为人名日报发布一月份关于疫情的微博信息\n")
    print("加载中,请等待...")
    a=open('comment_info.txt','r+')
    a.truncate(0)
    a.close()
    data = {
        'type': 'uid',
        'value': '2803301701',
        'containerid': '1076032803301701'
    }
    url = 'https://m.weibo.cn/api/container/getIndex?' + urlencode(data)
    main(url)

