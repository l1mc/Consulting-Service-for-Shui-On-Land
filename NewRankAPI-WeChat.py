# -*- coding: utf-8 -*-
"""
Created on Wed Aug 12 20:40:23 2020

@author: Mingcong Li
"""
# 规则：一篇文章消耗2unit
import requests
import json
import pandas as pd
import datetime


def req_data(account, start, end):  # 每调用一次这个function，就请求一个月的数据
    url_api='https://api.newrank.cn/api/sync/weixin/account/articles_content'
    headers={'Key':'这里填入新榜API的key'}
    body={'account':account,'from':start,'to':end, 'page':'1', 'size':'1999'}
    response=requests.post(url_api,data=body,headers=headers)
    global data_month
    data_month = response.json()


# 一、请求数据
req_data('shanghaifabu','2020-07-1 00:00:00','2020-08-1 00:00:00')
original_document = data_month

date1 = '2020-8-1 00:00:00'
start = datetime.datetime.strptime(date1, '%Y-%m-%d %H:%M:%S')
delta = datetime.timedelta(days=3)
n_days = start + delta
print(type(n_days.strftime('%Y-%m-%d %H:%M:%S')))


# 二、计算循环次数
start = '2015-01-01 00:00:00'
end = '2020-08-23 00:00:00'
start = datetime.datetime.strptime(start, '%Y-%m-%d %H:%M:%S')
end = datetime.datetime.strptime(end, '%Y-%m-%d %H:%M:%S')
delta = end - start
times = int(delta.days/31) + 1

# 三、循环抓取内容
data_all_df = pd.DataFrame()
account='sinacaijing'
start_sub = start
delta = datetime.timedelta(days=31)
end_sub = start_sub + delta
# i的取值从1到times，步长为1
for i in range(1,times+1,1):
    print('正在进行第%i次请求，请求的数据来自于%s-%s' %(i,start_sub,end_sub))
    req_data(account,start_sub.strftime('%Y-%m-%d %H:%M:%S'),end_sub.strftime('%Y-%m-%d %H:%M:%S'))
    data = data_month['data']
    for item in data:
        data_all_df = data_all_df.append([item], ignore_index=True)
    # 更新时间段
    start_sub = start_sub + delta
    end_sub = end_sub + delta

# 四、保存
data_all_df
data_all_df.to_csv('output_v2.csv')