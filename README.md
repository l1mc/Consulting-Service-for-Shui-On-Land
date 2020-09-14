# Consulting-Service-for-Shui-On-Land
This repository stores the programs I wrote while providing consulting services for Shui On Land.  

## My Job in This Project
* We helped our client, Shui On Land, to find high-net-worth individuals in Shanghai, making it easier for our client to grasp their needs.
* My job was to do data and text analysis. Also, I took the initiative to provide my boss with several financial perspectives to gain an insight.
* I analyzed the rise and fall of various industries from the perspective of online public opinion, listing conditions, and senior executives' annual salary data.  

## Public Opinion - Wechat & Douyin
* [NewRankAPI-WeChat.py](https://github.com/l1mc/Consulting-Service-for-Shui-On-Land/blob/master/NewRankAPI-WeChat.py): To use NewRank API to download and save information -- such as likes, comments, reads, pulish time, text -- about aritles in WeChat official account.  
* [NewRankAPI-Douyin.py](https://github.com/l1mc/Consulting-Service-for-Shui-On-Land/blob/master/NewRankAPI-Douyin.py): To use NewRank API to download and save information -- such as watches, comments, music, title -- about videos in Douyin.  

## Public Opinion - Xueqiu
* [TF-IDF.py](https://github.com/l1mc/Consulting-Service-for-Shui-On-Land/blob/master/TF-IDF.py): I screened out content about Shanghai from 270,000 articles and produced TF-IDF. Then my boss used a clustering algorithm to summarize the four most frequently appeared industries.
* [Word frequency changes.py](https://github.com/l1mc/Consulting-Service-for-Shui-On-Land/blob/master/Word%20frequency%20changes.py): According to the four most frequently appeared industries, I analyzed the changes in the frequency of words appearing in the news of each industry.

## Listing Conditions
* [Listing.py](https://github.com/l1mc/Consulting-Service-for-Shui-On-Land/blob/master/Listing.py): To analyze the number of new listed companies in different industries each year. Our assumptions is that the industry that has gradually increased the number of annual listings is the sunrise industry. There are more high-net-worth individuals in these industries.
* The outcome of the analysis of listing conditions are several figures. Below is a sample.
<img src = 'https://ftp.bmp.ovh/imgs/2020/09/dcfd91dcbabba59d.png' width="50%">

## The annual salary of directors and senior management
* They are high-net-worth individuals and potential customers of Shui On.
* In industries where directors and executives are at a new high, generally speaking, the middle management will also have a stronger economic strength.
* I found the data from Wind.
