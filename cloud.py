#-*- coding: utf-8 -*-
from wordcloud import WordCloud
import jieba
import numpy as np
import PIL.Image as Image
class Get_cluod():
    def __init__(self,text):
        self.text=text
    def get_show(self):
        mask_pic=np.array(Image.open("bg.jpg"))
        wordcloud = WordCloud(font_path="C:/Windows/Fonts/simfang.ttf",#设置字体
                              mask=mask_pic,#设置背景图片
                              background_color="white",#设置背景颜色
                              max_font_size=150,# 设置字体最大值
                              max_words=2000, # 设置最大显示的字数
                               stopwords={'Python'}, #设置停用词，停用词则不再词云图中表示
                              ).generate(self.text)
        image=wordcloud.to_image()
        wordcloud.to_file('comment_cloud.png')
        print("图片已经下载")
        image.show()

