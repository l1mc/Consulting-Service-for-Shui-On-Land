# -*- coding: utf-8 -*-
"""
Created on Thu Aug 27 09:56:51 2020

@author: Mingcong Li
"""

import codecs
import jieba
from gensim import corpora, models, similarities
import pandas as pd
import numpy as np


df = pd.read_csv(r'D:\total_df.csv')
stop_words = 'D:\停用词表.txt'
stopwords = codecs.open(stop_words, 'r', encoding='utf-8').readlines()
stopwords = [w.strip() for w in stopwords]
df=df.dropna(axis=0,how='any',inplace=False)
df=df[df['content'].str.contains('上海|沪')]
df.to_csv(r'D:\shanghai_df.csv')


i=0
books_list = []
for item in df.content.values:
    i +=1
    try:
        book_list = [word for word in jieba.cut(item) if word not in stopwords]
        books_list.append(book_list)
    except:
        print(i)
        continue

type(books_list)
books_list[10]
# （1）通过corpora.Dictionary方法建立字典对象
dictionary = corpora.Dictionary(books_list)
type(dictionary)
# （2）使用dictionary.doc2bow方法构建词袋(语料库)
corpus = [dictionary.doc2bow(stu) for stu in books_list]  # 元组中第一个元素是词语在词典中对应的id，第二个元素是词语在文档中出现的次数
type(corpus)
corpus[152]
# （3）使用models.TfidfModel方法对语料库建模
tfIdf_model = models.TfidfModel(corpus)
tfIdf_model.save(r"D:\my_model.tfidf")  # 保存模型
tfIdf_model = models.TfidfModel.load(r"D:\my_model.tfidf")
# corpus = [dictionary.doc2bow(book) for book in books_list]

i = 0
for tfidf in tfIdf_model[corpus]:
    print(tfidf)
    i += 1
    if i > 5:
        break





index = similarities.SparseMatrixSimilarity(tfIdf_model[corpus], num_features=len(dictionary.keys()))
type(index)

sim = index[tfIdf_model[corpus]]
type(sim)
sim.shape
sim[0:10,0:10]

np.save("sim.npy",sim)


b = np.load("sim.npy")

b[0:10,0:10]
