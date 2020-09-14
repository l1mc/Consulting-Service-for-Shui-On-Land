# -*- coding: utf-8 -*-
"""
Created on Tue Sep  1 20:57:29 2020

@author: Mingcong Li
"""

import pandas as pd
import numpy as np
import os
import jieba
import codecs
import copy
import json


# 分词的函数
def cut_word(word):
    cw = [item for item in jieba.cut(word, cut_all=False) if item not in stopwords]
    return cw


# ngram的函数
# 第一个参数是分好词的tokens。第二个参数是停止词，如果在停止词里面的不加入到ngram里面。第三个参数是几个词一组。
def word_ngrams(tokens, stop_words=None,ngram_range=(1,1)):
        """Turn tokens into a sequence of n-grams after stop words filtering"""
        # handle stop words
        if stop_words is not None:
            tokens = [w for w in tokens if w not in stop_words]

        # handle token n-grams
        min_n, max_n = ngram_range
        if max_n != 1:
            original_tokens = tokens
            tokens = []
            n_original_tokens = len(original_tokens)
            for n in range(min_n,
                            min(max_n + 1, n_original_tokens + 1)):
                for i in range(n_original_tokens - n + 1):
                    tokens.append(" ".join(original_tokens[i: i + n]))

        return tokens


# 统计词频的函数。
# 第一个参数是存放数据的dataframe，第二个参数是用于筛选新闻标题的关键词，第三个参数是分好词的数据再哪一列。
def freq(dataframe,keywords,col):
    df_keywords=dataframe[dataframe['content'].str.contains(keywords)]
    frequency = pd.Series(df_keywords[col].sum()).value_counts()
    return frequency


# 批量计算4个行业的词频的函数
# 输入值为ngram所在的列名
# 输出顺序为：总的、长三角、5G、AI、生物医药
def outc(dataframe, col):
    total = freq(dataframe,kw_total,col)  # 统计词频·总。返回的是pandas.core.series.Series类型
    YDR = freq(dataframe,kw_YDR,col)  # 统计词频·长三角
    fg = freq(dataframe,kw_5g,col)  # 统计词频·5g
    ai = freq(dataframe,kw_ai,col)  # 统计词频·人工智能
    bm = freq(dataframe,kw_bm,col)  # 统计词频·生物医药
    return [total,YDR,fg,ai,bm]


# 生成关键词的排名变化
def gen_change(compare):
    if compare > 20:
        return 'new'
    elif compare >0:
        return 'upward'
    elif compare == 0:
        return 'unchanged'
    elif compare > -20:
        return 'downward'
    else:
        return 'disappeared'


# 准备停用词
global stop_words
stop_words = 'D:\桌面的文件夹\实习\睿丛\产业研究\停用词表.txt'
stopwords = codecs.open(stop_words, 'r', encoding='utf-8').readlines()
stopwords = [w.strip() for w in stopwords]
stopwords.extend(['上海','上海市','沪',' ','','日','月','1%','2%','10'])  # 这些词频统计，没有意义。根据后面的数据分析找出来的。
stopwords.extend(['两市','公司','点','指','亿元','指涨','指跌','年','震荡','大涨','指数','早盘'])  # 由1gram步骤找到的停止词。这些词频率高是由雪球这个网站的特性导致，不能产生关于行业的insight。
stopwords.extend(['概念','深成指','创业板','有限公司','股份','净','买入','股','深证','午评','集体','全线','三大','午后','股指','板块','涨幅','跌幅','居前','掀','涨停','潮','跌','涨','股指','北上','资金','截止','收盘','展开','板块','今日','收盘'])  # 由2gram和3gram步骤找到的停止词。这些词频率高是由雪球这个网站的特性导致，不能产生关于行业的insight。
stopwords[-50:]


# 导入数据
os.chdir(r'D:\桌面的文件夹\实习\睿丛\产业研究')
shanghai_df = pd.read_csv('shanghai_df.csv')
shanghai_df.head(2)
shanghai_df.info()
shanghai_df.describe()
df = copy.deepcopy(shanghai_df)  # 复制一份原始数据

# 分词
# 1gram结果。用jieba。
df['tokenized'] = df['content'].apply(cut_word)
# 2gram结果。用自己的function。
df['2gram'] = list(map(lambda x: word_ngrams(tokens = x,ngram_range=(2,2)), df['tokenized']))
# 3gram结果。用自己的function。
df['3gram'] = list(map(lambda x: word_ngrams(tokens = x,ngram_range=(3,3)), df['tokenized']))

# 定义用于筛选的关键词
kw_total='5G|5g|人工智能|生物医药|长三角|长江三角洲|医药|生物|AI|江浙沪'
kw_YDR='长三角|长江三角洲|江浙沪'
kw_5g='5g|5G'
kw_ai='人工智能|AI'
kw_bm='生物医药|医|药|生物'

# 统计词频。下面三行分别计算1gram、2gram、3gram
# 每一次调用的输出顺序为：总的、长三角、5G、AI、生物医药
one_gram=outc(df,'tokenized')  # 最外层是list，里面的元素是Series
two_gram=outc(df,'2gram')
three_gram=outc(df,'3gram')

two_gram[1][0:10]




# 时间切片


# 计算每一年的5个行业，它们的1gram, 2gram, 3gram
# 返回值为一个列表，这个列表的每一个元素也是一个列表，为1gram, 2gram, 3gram。每一个元素下面的子元素是Series，分别为5各行业。子元素下面的孙元素是最内层了，是每一个词的词频。
# 输入为一个字符串，别输入成int了
def subyear(year):
    df_temp=df[df['time'].str.contains(year)]
    one_gram=outc(df_temp,'tokenized')  # 最外层是list，里面的元素是Series
    two_gram=outc(df_temp,'2gram')
    three_gram=outc(df_temp,'3gram')
    return [one_gram,two_gram,three_gram]

test=subyear('2018')
len(test)  # 长度为3，表示3个gram长度
len(test[0])  # 长度为5，表示5个行业类型
len(test[0][0])  # 长度为3832，表示3832个关键词
test[1][1][0:10]
# 第一个参数为[0,1,2]，分别表示：1gram, 2gram, 3gram
# 第二个参数为[0,1,2,3,4]，分别表示：总的、长三角、5G、AI、生物医药
# 第三个参数表示取频率前10高的


# 生成f_2016到f_2020，分别是每一年的3中gram的5个行业分类的词频。



# 生成一些新的子df，这些子df用于比较变化keywords的变化。
# 第一个参数为要处理的总的dataframe。
# 第二个参数为这个总的dataframe对应的年份。
# 第三个参数为要提取的是多少gram的关键词。取值范围为[0,1,2]，分别表示：1gram, 2gram, 3gram
# 第四个参数为要提取哪一个行业的。取值范围为[0,1,2,3,4]，分别表示：总的、长三角、5G、AI、生物医药
def gen_df(dataframe,year,ngram,industry):
    dataframe = dataframe[ngram][industry][0:40].to_frame().reset_index().reset_index()
    dataframe.columns=['rank_%s' %year,'keyword','frequency_%s' %year]
    dataframe=dataframe.set_index(["keyword"], inplace=False)
    return dataframe


# 合并、整理，输出keywrod的变化情况
def Mer_Org(dataframe1,dataframe2):
    # 合并，把NAN转成999
    df_temp=pd.concat([dataframe1,dataframe2], axis=1).fillna(999)
    # 两年的rank做差
    df_temp['compare']=df_temp.iloc[:,[0]].values-df_temp.iloc[:,[2]].values
    # 差转换成字符
    df_temp['outcome']=list(map(lambda x: gen_change(x), df_temp['compare']))
    # 输出关键词的变化
    list_type=['unchanged','upward','downward','disappeared','new']
    for item in list_type:
        temp=df_temp['outcome'].loc[df_temp['outcome'].isin([item])].index.values
        print('The %s keywards are: ' %item,temp)
    return



# 打印所有的结果
list_industry=['four_total','Yangtze River Delta','5G','AI','biomedicine']
list_ngram=['1gram','2gram','3gram']
for industry in range(0,5,1):
    print('----------Below is the analysis of the ',list_industry[industry],' industry.----------')
    for ngram in range(0,3,1):
        print('-------Below is the [',list_ngram[ngram],'] analysis of the ',list_industry[industry],' industry.-------')
        df_2016=gen_df(subyear('2016'),'2016',ngram,industry)
        df_2017=gen_df(subyear('2017'),'2017',ngram,industry)
        df_2018=gen_df(subyear('2018'),'2018',ngram,industry)
        df_2019=gen_df(subyear('2019'),'2019',ngram,industry)
        df_2020=gen_df(subyear('2020'),'2020',ngram,industry)
        print('-----Changes in 2020 compared to 2019-----')
        Mer_Org(df_2019,df_2020)
        print('-----Changes in 2019 compared to 2018-----')
        Mer_Org(df_2018,df_2019)
        print('-----Changes in 2018 compared to 2017-----')
        Mer_Org(df_2017,df_2018)
        print('-----Changes in 2017 compared to 2016-----')
        Mer_Org(df_2016,df_2017)
        print()
    print()
    print()


# 保存所有的词频
list_industry=['four_total','Yangtze River Delta','5G','AI','biomedicine']
list_ngram=['1gram','2gram','3gram']
for industry in range(0,5,1):
    for ngram in range(0,3,1):
        df_2016=gen_df(subyear('2016'),'2016',ngram,industry)
        df_2017=gen_df(subyear('2017'),'2017',ngram,industry)
        df_2018=gen_df(subyear('2018'),'2018',ngram,industry)
        df_2019=gen_df(subyear('2019'),'2019',ngram,industry)
        df_2020=gen_df(subyear('2020'),'2020',ngram,industry)
        df_2016.to_csv("%s-2016-%s.csv" %(list_industry[industry],list_ngram[ngram]),encoding = 'utf_8_sig')
        df_2017.to_csv("%s-2017-%s.csv" %(list_industry[industry],list_ngram[ngram]),encoding = 'utf_8_sig')
        df_2018.to_csv("%s-2018-%s.csv" %(list_industry[industry],list_ngram[ngram]),encoding = 'utf_8_sig')
        df_2019.to_csv("%s-2019-%s.csv" %(list_industry[industry],list_ngram[ngram]),encoding = 'utf_8_sig')
        df_2020.to_csv("%s-2020-%s.csv" %(list_industry[industry],list_ngram[ngram]),encoding = 'utf_8_sig')



































# 保存ngram结果
os.chdir(r'D:\ngram')
name=['总的','长三角','5G','AI','生物医药']
i=0
for item in one_gram:
    n=name[i]
    item.to_csv("1gram-%s.csv" %n,encoding = 'utf_8_sig')
    i +=1

i=0
for item in two_gram:
    n=name[i]
    item.to_csv("2gram-%s.csv" %n,encoding = 'utf_8_sig')
    i +=1

i=0
for item in three_gram:
    n=name[i]
    item.to_csv("3gram-%s.csv" %n,encoding = 'utf_8_sig')
    i +=1



# 导入数据
df = pd.read_csv(r'D:\shanghai_df_tokenized.csv')
# 这里有一个问题:重新导入的数据,每一行都会作为str,而不是list导入

# 去除'上海'这个关键词。这个作为词频统计，没有意义
df['tokenized'] = list(map(lambda x: x.replace("\'上海\', ", ''), df['tokenized']))

# 去除'沪'这个关键词
df['tokenized'] = list(map(lambda x: x.replace("\'沪\', ", ''), df['tokenized']))
# map()里面的第一个参数是要执行的function，第二个参数是一个可迭代对象。可以实现对第二个参数里面的每一个子元素，都执行第一个参数中的function。注意，返回的内容一定要在外面套上list()。
# 引号要用转义符\。
# 匿名函数中，冒号前面表示要传入的参数，冒号后面表示要对这个参数执行的操作。
# .replace()这个函数的第一个参数是要背替换掉的内容，第二个参数是要替换成什么