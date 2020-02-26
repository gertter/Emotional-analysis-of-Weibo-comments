#-*- coding: utf-8 -*-
from snownlp import SnowNLP
import jieba
from tabel import Table
from cloud import Get_cluod
import logging
jieba.setLogLevel(logging.INFO)
def get_word():
    d={}
    all=''
    result=[]
    with open("comment_info.txt",'r') as f:
        for i in f.readlines()[1:-1]:
            all+=i
        word=jieba.lcut(all)
        for i in word:
            d[i] = d.get(i, 0) + 1
        txts = list(d.items())
        txts.sort(key=lambda x: x[1], reverse=True)
        for l in txts:
            if l[0]=='\n' or l[0]=='，' or l[0]=='!' or len(l[0])<2:
                pass
            else:
                result.append(l[0])
    f.close()
    return result
def get_all():
    with open("comment_info.txt",'r') as f:
        for i in f.readlines()[1:-1]:
            print(i)
    f.close()
def get_title():
    with open("comment_info.txt",'r') as f:
        print(f.readlines()[0])
    f.close()
def get_ever_word():#每一句话的平均分
    list=[]
    key=1
    avder_list=[]
    all=0.0
    with open("comment_info.txt",'r') as f:
        for i in f.readlines()[1:-1]:
            i.replace('\n','')
            print("第"+str(key)+"条评论")
            print("内容:"+i)
            word = jieba.lcut(i)
            if len(word)==0:
                pass
            else:
                for l in word:
                    if l=='\n' or l=='，' or l=='!' or len(l)<2:
                        pass
                    else:
                        j=get_movig(l)
                        list.append(j)
                if len(list)==0:
                    pass
                else:
                    print("词得分")
                    print(list)
                    for i in list:
                        all+=i['分值']
                    avger=all/len(list)
                    avder_list.append(avger)
                    print("平均分"+str(round(avger,5)))
                list=[]
                key+=1
                all=0.0
    return avder_list
    f.close()
def get_avger_table():#每一个评论的图
    list = get_ever_word()
    get_table(list)
def get_table(list):#图表显示
    X=''
    for i in range(1,len(list)+1):
        X+=str(i)
    a = Table(len(list),tuple(list),X)
    a.get_show()
def get_movig(word):
    s = SnowNLP(word)
    s.tags
    p = s.sentiments
    p1=round(p,3)
    data={
        "分值":p1,
        "词汇":word,
    }
    return data
def get_all_avger():
    score = []
    all_score = 0
    list = get_word()
    for word in list:
        word_score = get_movig(word)
        all_score += word_score['分值']
        score.append(word_score)
    avger = all_score / len(score)
    print(avger)
def get_cluod(text):
    a = Get_cluod(text)
    a.get_show()
def get_word_all():
    list = get_word()
    word=''
    for i in list:
        word+=" ".join(i)
    get_cluod(word)
if __name__=='__main__':
    a = open('comment_info.txt', 'r')
    if len(a.readlines())==0:
        print("请先运行get_commnet.py获取你想要的评论")
        a.close()
    else:
        print("***微博标题****")
        get_title()
        print("查看所有评论内容输入all")
        print("查看每一个评论的情绪得分输入comment")
        print("查看每一评论分值图表输入table")
        print("查看词云图输入cloud")
        print("查看所有评论平均得分输入average")
        key = input("请输入:")
        if key=='all':
            get_all()
        if key=='comment':
            get_ever_word()
        if key=='table':
            get_avger_table()
        if key=='cloud':
            get_word_all()
        if key == 'average':
            get_all_avger()


