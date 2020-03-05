# coding=utf-8

import pandas as pd

import matplotlib.pyplot as plt
import matplotlib

df = pd.read_excel("C:\\Users\\lenovo\\Documents\\data\\豆瓣电影Top250.xls")

matplotlib.rcParams['font.family'] = 'SimHei'
matplotlib.rcParams['font.size'] = '20'

plt.figure(figsize=(20, 5))
plt.subplot(1, 2, 1)  # 一行两列，第一个子图
plt.scatter(df['评分'], range(1, 251))  # 评分的范围
plt.xlabel('评分')
plt.ylabel('排名')

plt.gca().invert_yaxis()  # 改y轴为倒序

# 集中趋势的直方图
plt.subplot(1, 2, 2)  # 一行两列，第二个子图
plt.hist(df['评分'], bins=15)  # 取评分列，画15个条形图，数据中评分范围是8.3-9.7正好15个评分
# print(df.head())
#
# print("-------------------------")
#
# print(df.info())
plt.show()
