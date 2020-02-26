#-*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np
class Table():
    def __init__(self,N,info,X):
        self.N=N
        self.score=info
        self.X=X
        plt.rcParams['font.sans-serif'] = ['STSong']
    def get_show(self):
        plt.figure(figsize=(10, 10), dpi=80)
        N = self.N
        values = self.score#元祖
        index = np.arange(N)
        width = 0.45
        p2 = plt.bar(index, values, width, label="num", color="#87CEFA")
        plt.xlabel('评论')
        plt.ylabel('分值')
        plt.title('平均分')
        plt.xticks(index, ('评论'+str(i)for i in self.X))
        plt.legend(loc="upper right")
        plt.legend(['数据'])
        plt.show()
