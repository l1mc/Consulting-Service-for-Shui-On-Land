# -*- coding: utf-8 -*-
"""
Created on Mon Aug 17 14:28:27 2020

@author: Mingcong Li
"""
import difflib  # 计算两个字符串相似度的
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import copy  #用来深度复制
import matplotlib.ticker as mtick  # 用来改变坐标抽格式
plt.rcParams['font.sans-serif'] = ['FangSong'] # 指定默认字体
plt.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题


# 做分类汇总的函数
def pivot1(listn, version):
    # csv_data[csv_data['area'].isna()]
    subset = csv_data[csv_data['area'].isin(listn)]
    subset['list_date_short'] = subset['list_date'].apply(str).str[0:4]
    global result
    result = pd.crosstab(subset.list_date_short, subset.industry, margins = True)
    result.to_excel(r'D:\桌面的文件夹\实习\睿丛\output_%s.xls' %version)
    return


# 统计的三个层次
list1 = ['南京', '苏州', '无锡', '常州', '镇江', '扬州', '泰州', '南通', '淮安', '连云港', '盐城', '徐州', '宿迁', '杭州', '宁波', '温州', '绍兴', '湖州', '嘉兴', '金华', '衢州', '台州', '丽水', '舟山', '合肥 ', '马鞍山', '淮北', '宿州', '阜阳', '蚌埠', '淮南', '滁州', '六安', '巢湖', '芜湖', '亳州', '安庆', '池州', '铜陵', '宣城', '黄山', '上海', '江苏', '安徽', '浙江']
list2 = ['南京', '苏州', '无锡', '常州', '镇江', '扬州', '泰州', '南通', '淮安', '连云港', '盐城', '徐州', '宿迁', '杭州', '宁波', '温州', '绍兴', '湖州', '嘉兴', '金华', '衢州', '台州', '丽水', '舟山', '上海', '江苏', '浙江']
list3 = ['上海']


# 导入数据
csv_file = r'D:\桌面的文件夹\实习\睿丛\分年份、分行业统计长三角地区当年上市数量\df_stock.csv'
csv_data = pd.read_csv(csv_file, low_memory = False)#防止弹出警告
print(csv_data)
csv_data.info()
csv_data.head()
csv_data.describe()
csv_data.head(50)


# 进行三个层次的分类汇总
pivot1(list1,'list1')
pivot1(list2,'list2')
pivot1(list3,'list3')

result  # 查看分类汇总的结果



# 处理行业名称
# 准备好申万行业分类的数据
Tpye=pd.read_excel(r'D:\桌面的文件夹\实习\睿丛\分年份、分行业统计长三角地区当年上市数量\申银万国行业分类标准 .xlsx',sheet_name='处理', header=None)  # 导入行业分类
type1 = Tpye.sort_values(1, axis=0)  # 按照行业编号有小到大排序
type1=type1.drop_duplicates(subset=0, keep='first', inplace=False, ignore_index=False)  # 去除重复行。有些母分类和子分类是同名的，就只保留母分类。
type1=type1.rename(columns={0:'industry'})  # 给行业名称的列命名。
type1=type1.rename(columns={1:'code'})  # 给行业名称的列命名。
type1 = type1.set_index("industry")  # 让行业名称成为行标签，便于后续合并
print(type1.index.is_unique)  # 发现行标签没有重复的
type1

# 在最前面插入一个空列，用来保存匹配的结果
test=result.T.iloc[0:79,:]  # 取消行业类型里面的“all”
col_name=test.columns.tolist()  # 将数据框的列名全部提取出来存放在列表里
col_name.insert(0,'new')  # 在列索引为0的位置插入一列,列名为:new，刚插入时不会有值，整列都是NaN
test=test.reindex(columns=col_name)  #  DataFrame.reindex() 对原行/列索引重新构建索引值
test


#  把申万分类匹配到原始分类上
test.iloc[:,0] = test.index.map(lambda x: difflib.get_close_matches(x, type1.index, cutoff=0.3,n=1)[0])  # map()就是对于一个可迭代对象中的元素，轮流执行一个function
test.head(60)  # 查看匹配结果
test.iloc[61:81,:]  # 查看匹配结果
test.to_excel(r'D:\桌面的文件夹\实习\睿丛\行业分类匹配结果.xls')  # 导出匹配结果，手工在excel里面处理匹配不正确的项目。发现有11个需要手工调整


# 把行业名称转换为申万的命名体系。
#导入并整理
data=pd.read_excel(r'D:\桌面的文件夹\实习\睿丛\行业分类匹配结果_修改后.xls', index_col = 'industry')  # 重新导入匹配好分类的行业汇总
data = data.groupby(data.index).sum()  # 把重复的行业进行加和。因为concat要求index不能重复。注：此时子行业和母行业是混乱出现的。
# 合并
outcome = pd.concat([data, type1], axis=1, join='inner', ignore_index=False)  # 这里是按照index合并数据，可以合并object类型的。inner表示求交集，outer表示求并集。由于data里面的index是type1的子集，所以可以用inner方式。axis=1表示横向合并。
# 改行业代码
outcome['code'] = outcome['code'].apply(str).str[0:2].map(lambda x: x+'0000')  # 把行业代码改成一级行业的代码，即后四位全是0
outcome['code'] = outcome['code'].astype('int64')
# 生成新的index
outcome1 = outcome.set_index('code')
outcome1 = outcome1.groupby(outcome1.index).sum()
type2 = type1.reset_index().set_index('code')  # 把原来作为index的‘industry’还原成一列数据
outcome2 = pd.concat([outcome1, type2], axis=1, join='inner', ignore_index=False)  # 把申万的中文一级行业名称匹配到数据上。这个地方一定要注意，index的数据类型也必须一致，否则合并不出来。
result = outcome2.set_index('industry').T
row_name=result.index.tolist()  # 将数据框的列名全部提取出来存放在列表里
type(row_name[1])  # 确认是字符型元素
row_name.insert(1,'1991')  # 在列索引为1的位置插入一行,行名为:1991。因为前面的分类汇总会导致一些没有上市的年份被省略掉。
row_name.insert(15,'2005')
row_name.insert(-8,'2013')
result=result.reindex(index=row_name)  #  DataFrame.reindex() 对原行/列索引重新构建索引值
result.iloc[[1, 15, -9],:]=0.0  # 把NaN的值填充成零
result  # result是整理完的总的数据集
# 到这里，数据的整理就完成了。







# 下面开始分析数据
nameDF = pd.DataFrame()  # # 空df储存分析类型、行业名称
# 提取分行业的上市总量，用于1和2
industry = result[31:32]  # 提取最后一行加总的值ALL
# 1.上市数量最多的10个行业
# 提取
temp1 = industry.T.sort_values('All',ascending=False,inplace=False)[0:11]  # 提取行业名称以及上市数量
temp1
# 画图
title='过去30年上市数量最多的10个行业'  # 单独设置title，一遍存储到nameDF中
fig1 = temp1.plot(kind='bar', fontsize=16, figsize=(14,14*0.618), title=title, rot=0, legend='')  #设置图的格式
fig1.axes.title.set_size(20)  #设置标题
# 储存
fig1.figure.savefig(r'D:\桌面的文件夹\实习\睿丛\过去30年上市数量最多的10个行业.png')  #保存图片
type(temp1)  # 查看temp1的类型
stri='，'  # 设置分隔符
seq=temp1.index.tolist()  # 获取行业名称
industryName = stri.join(seq)  # 把列表中的所有元素合并成一个字符串。
s = pd.Series([title,industryName])  #保存标题和行业名称
nameDF = nameDF.append(s, ignore_index=True)  # 添加到df中


# 2.上市数量最少的10个行业。这里的代码比1可复制性更高。
# 提取
temp2 = industry.T.sort_values('All',ascending=True,inplace=False)[0:11].sort_values('All',ascending=False,inplace=False)  # 和1一样的规则。提取行业名称以及上市数量。先从小到大提取前10，再把筛选出来的从大到小排。
# 画图
title='过去30年上市数量最少的10个行业'  # 单独设置title，一遍存储到nameDF中
fig2 = temp2.plot(kind='bar', fontsize=16, figsize=(14,14*0.618), title=title, rot=0, legend='')  #设置图的格式
fig2.axes.title.set_size(20)  #设置标题
fmt='%.0f'
yticks = mtick.FormatStrFormatter(fmt)
fig2.yaxis.set_major_formatter(yticks)  # 设置不要有小数位数。dataframe里面每一个数都是浮点型的。
# 储存
fig2.figure.savefig(r'D:\桌面的文件夹\实习\睿丛\%s.png' %title)  #保存图片
seq=temp2.index.tolist()  # 获取行业名称
industryName = stri.join(seq)  # 把列表中的所有元素合并成一个字符串。
s = pd.Series([title,industryName])  #保存标题和行业名称
nameDF = nameDF.append(s, ignore_index=True)  # 添加到df中


# 3.提取分年度的上市总量
# 提取
result['All'] = result.apply(lambda x: x.sum(),axis=1)  # 增加每一行的汇总值，下面一步提取的就是这个值
# 画图
title='上海地区过去30年每年的上市数量变化'
temp3= result.iloc[:,-1].drop(['All'])
fig3 = temp3.plot(kind='line', fontsize=16, figsize=(14,14*0.618),use_index=True, title=title, rot=0)
fig3.axes.title.set_size(20)
# 储存
fig3.figure.savefig(r'D:\桌面的文件夹\实习\睿丛\%s.png' %title)   #保存图片


# 年份合并，来平滑波动
result4 = result.iloc[:-1,:]
# 4.五年一合并，绝对数
i = 0
data_new = pd.DataFrame()
while i < (result.shape[0]-1):
    try:
        data_new = data_new.append(result4.iloc[i,:]+result4.iloc[i+1,:]+result4.iloc[i+2,:]+result4.iloc[i+3,:]+result4.iloc[i+4,:], ignore_index=True)
    except:
        i +=5
    i +=5
s=data_new.sum(axis=0)
data_new = data_new.append(s, ignore_index=True)
data_new
# 提取
title='上市总数最多的12个行业的上市数量'
temp4 = data_new.T.sort_values(by=[6],ascending=False,inplace=False).iloc[0:12,:-1].T
# 画图
fig4 = temp4.plot(kind='line', subplots=True,sharex=True, sharey=True, fontsize=16, layout=(3,4),figsize=(18,18*0.618),use_index=True, title=title, legend=True, rot=90)
labels = ['1990-1994', '1995-1999', '2000-2004', '2005-2009', '2010-2014','2015-2019']  # 设置标签的名称
x = np.arange(len(labels))  # the label locations
fig4[1,1].set_xticks(x)  # 设置刻度
fig4[1,1].set_xticklabels(labels)  # 设置刻度的名称
fmt='%.0f'
yticks = mtick.FormatStrFormatter(fmt)
fig4[1,1].yaxis.set_major_formatter(yticks)  # 设置不要有小数位数。dataframe里面每一个数都是浮点型的。
# 储存
fig4[1,1].figure.savefig(r'D:\桌面的文件夹\实习\睿丛\%s.png' %title)   #保存图片，这里，fig4是一个AxesSubplot对象，实际形式是一个ndarray。因此，只要调用这个ndarray里面的任何一个图像，就能把所有的图片画出来。注意，这一调用的是第二行、第二列的图片。
fig4[0,0].figure.show()
seq=temp4.T.index.tolist()  # 获取行业名称
industryName = stri.join(seq)  # 把列表中的所有元素合并成一个字符串。
s = pd.Series([title,industryName])  #保存标题和行业名称
nameDF = nameDF.append(s, ignore_index=True)  # 添加到df中


# 5.五年一合并，相对数
# 准备加总数
data_reg = copy.deepcopy(data_new)  #这里需要一个深度复制，保持Df是不变的。否则如果运行一次程序要连着查好几次，就会出问题。因为我们要对Df的格式整个进行改变。
data_reg['All']=data_reg.sum(axis=1)  # 每一年所有行业的上市量求和，放在最后一列。每个行业的加总已经有了，在第六行。
# 求相对数
data_reg=data_reg.div(data_reg.iloc[:,-1],axis=0).iloc[:,:-1]  # 用来回归的数据集，是相对数

# 提取
title='上市总数最多的12个行业的上市占比'
temp5 = data_reg.T.sort_values(by=[6],ascending=False,inplace=False).iloc[0:12,:-1].T
# 画图
fig5 = temp5.plot(kind='line', subplots=True,sharex=True, sharey=True, fontsize=16, layout=(3,4),figsize=(18,18*0.618),use_index=True, title=title, legend=True, rot=90)
labels = ['1990-1994', '1995-1999', '2000-2004', '2005-2009', '2010-2014','2015-2019']  # 设置标签的名称
x = np.arange(len(labels))  # the label locations
fig5[1,1].set_xticks(x)  # 设置x轴刻度
fig5[1,1].set_xticklabels(labels)  # 设置x轴刻度的名称
fig5[1,1].yaxis.set_major_formatter(mtick.PercentFormatter(1,0))  # 设置y轴的格式为没有小数点的百分比。第一个参数为把多少的数值设置为100%，第二个参数为保留几位小数。
# 储存
fig5[1,1].figure.savefig(r'D:\桌面的文件夹\实习\睿丛\%s.png' %title)   #保存图片，这里，fig4是一个AxesSubplot对象，实际形式是一个ndarray。因此，只要调用这个ndarray里面的任何一个图像，就能把所有的图片画出来。注意，这一调用的是第二行、第二列的图片。
fig5[0,0].figure.show()
seq=temp5.T.index.tolist()  # 获取行业名称
industryName = stri.join(seq)  # 把列表中的所有元素合并成一个字符串。
s = pd.Series([title,industryName])  #保存标题和行业名称
nameDF = nameDF.append(s, ignore_index=True)  # 添加到df中


# 做回归进行分类

# 设置好X、Y、模型
Y_train=data_reg.iloc[:-1,:].T
X_train = pd.DataFrame(np.arange(6).reshape((-1, 1)))
from sklearn.linear_model import LinearRegression
linreg = LinearRegression()
# 开始训练
i=0
box=np.array([])
while i < (Y_train.shape[0]):
    print(i)
    linreg.fit(X_train, Y_train.iloc[i,:])
    i +=1
    box = np.hstack((box, linreg.coef_))

# 训练结果
print(box)
Y_train[6] = box

# 画图
# 增长最快的15个行业
temp11 = Y_train.sort_values(by=[6],ascending=False,inplace=False).iloc[:15,:-1].T
fig11 = temp11.plot(kind='line', ax=None, subplots=True,sharex=True, sharey=True, fontsize=16, layout=(3,5),figsize=(18,18*0.618),use_index=True, title='# 增长最快的15个行业', grid=None, legend=True,style= None, logx=False, logy=False,  loglog=False, xticks=None, yticks=None, xlim=None, ylim=None, rot=0, xerr=None,secondary_y=False, sort_columns=False)

# 衰退最快的15个行业
temp12 = Y_train.sort_values(by=[6],ascending=True,inplace=False).iloc[:15,:-1].T
fig12 = temp12.plot(kind='line', ax=None, subplots=True,sharex=True, sharey=True, fontsize=16, layout=(3,5),figsize=(18,18*0.618),use_index=True, title='增长前15的行业', grid=None, legend=True,style= None, logx=False, logy=False,  loglog=False, xticks=None, yticks=None, xlim=None, ylim=None, rot=0, xerr=None,secondary_y=False, sort_columns=False)


