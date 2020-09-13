# -*- coding: utf-8 -*-
"""
Created on Fri Aug 14 16:05:05 2020

@author: Mingcong Li
"""

import requests
import json
import time
import win32api,win32con
import pandas as pd

# 一、获取taskid
url_api='https://api.newrank.cn/api/async/task/douyin/history'
headers={'Key':'这里填入新榜API的key'}
body={'uid':'67374200959','from':'2020-08-10','to':'2020-08-16'}  # 这里的UID要从https://xd.newrank.cn/data/tiktok/account这个网站上查，不是抖音号。
response=requests.post(url_api,data=body,headers=headers)
htmls=response.text
print(htmls)  # 从这里复制taskID，填到第二步的data中


# 二、请求抖音作品信息
# 请求头
url_api='https://api.newrank.cn/api/task/douyin/result'
headers={'Key':'这里填入新榜API的key'}
data={'taskId':'3785b610-e03f-11ea-b0e4-00163e08419c', 'page':'1'}  # 上面返回的taskID填到这里。官方文档说，一个page返回20条作品

# 做一个循环，每隔10min请求一次，获得数据后弹出对话框提醒。
i = 0
while True:
    i = i + 1
    print('正在进行第%d次请求...' %i)
    response=requests.post(url_api,data=data,headers=headers)
    original_document = response.json()
    if original_document['code'] != 2202:
        break
    print('第%d次请求未采集到数据，10分钟后进行下一次请求' %i)
    time.sleep(600)
win32api.MessageBox(0, "抖音作品已经获取完毕!", "提醒",win32con.MB_OK)


# 三、清洗数据
print(original_document)  # 查看一下请求回来的原始数据
print(dict.keys(original_document))  # 发现是一个字典，查看传回来的字典有哪些key
print(original_document['data'])  # 发现有信息量的数据在data这个key里面
data1 = original_document['data']
print(data1)  # 发现打印出来是一个列表
print(len(data1))  # 看看这个列表里面有几个视频，发现是7个

data_sample = data1[1]  # 以第二个为例，查看其格式，发现是字典
print(dict.keys(data_sample))  # 查看一下有哪些key


# 四、储存数据
data = original_document['data']
data[0]
mydf = pd.DataFrame()
for item in data:
    mydf = mydf.append([item], ignore_index=True)
print(mydf)
mydf.to_csv(r'D:\excel_output.csv')
mydf.to_excel(r'D:\excel_output.xls')