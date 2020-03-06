# coding=utf-8

# 学习回顾：
#   1. 涉及到引用的工具包
#       a. 访问url使用requests库, 方法 requests.get()，需要加header否则会被反爬监测到返回418, response.text获取html
#       b. 使用正则表达式用re库, re.compile()编译, re.findall()匹配, re.sub()
#       c. 解析html使用BeautifulSoup，html.parser, soup.find_all()的使用
#       d. excel工具包使用xlwt, xlwt.Workbook() -> book.add_sheet() -> sheet.write() -> book.save():创建文档->创建sheet->写入数据->保存
#   2. 基础语法
#       a. Sting处理, 字符串截取方式str[a:b]，转换字符串str(), split()
#       b. 正则表达式的使用，占位符，匹配类型等
#       c. 循环语句，条件语句
#       d. 数组：拼接 list.append(), 插入元素 list.insert()
#   3. 访问url获取html

import sys
from bs4 import BeautifulSoup
import re
import requests

#不要使用pandas来处理Excel文件, 因为还是依赖xlrd的. 请直接使用openpyxl
#xlrd/xlwt不能处理Excel 2007之后的格式, 也就是说最大一张数据表仅支持65535行.
import xlwt

# 得到页面全部内容
def askURL(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0'}
    resp = requests.get(url, headers=headers)  # 必须是headers=headers 否则418
    html = resp.text
    # print(html)
    # print(resp.status_code)
    return html

# 获取相关内容
def getData(baseurl):
    findLink = re.compile(r'<a href="(.*?)">')  # 找到影片详情链接
    findImgSrc = re.compile(r'<img.*src="(.*?)"', re.S)  # 找到影片图片
    findTitle = re.compile(r'<span class="title">(.*)</span>')  # 找到片名
    findRating = re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')  # 找到评分
    findJudge = re.compile(r'<span>(\d*)人评价</span>')  # 找到评价人数
    findInq = re.compile(r'<span class="inq">(.*)</span>')  # 找到概况
    findBd = re.compile(r'<p class="">(.*?)</p>', re.S)  # 找到影片相关内容
    remove = re.compile(r'              |\n|</br>|\.*')  # 去掉无关内容
    datalist = []
    for i in range(0, 10):
        # 获取数据
        url = baseurl + str(i * 25)
        print("url is " + url)
        html = askURL(url)

        # 解析内容
        soup = BeautifulSoup(html, "html.parser")

        for item in soup.find_all('div', class_='item'):
            data = []  # 定义一个解析数据结果的列表
            item = str(item)  # 转换成字符串

            link = re.findall(findLink, item)[0]
            data.append(link)  # 添加详情链接

            imgSrc = re.findall(findImgSrc, item)[0]
            data.append(imgSrc)  # 添加图片链接

            titles = re.findall(findTitle, item)
            # 片名可能只有一个中文名，没有外国名
            if (len(titles) == 2):
                ctitle = titles[0]
                data.append(ctitle)  # 添加中文片名
                otitle = titles[1].replace("/", "")  # 去掉无关符号
                data.append(otitle)
            else:
                data.append(titles[0])  # 添加中文片名
                data.append(' ')  # 留空
            rating = re.findall(findRating, item)[0]
            data.append(rating)  # 添加评分
            judgeNum = re.findall(findJudge, item)[0]
            data.append(judgeNum)  # 评论人数
            inq = re.findall(findInq, item)
            # print(inq)
            # 添加概况 可能没有概况
            if len(inq) != 0:
                inq = inq[0].replace("。", "")  # 去掉句号
                data.append(inq)  # 添加概况
            else:
                data.append(' ')
            # print(re.findall(findBd, item))
            bd = re.findall(findBd, item)[0]
            # print("bd is "+bd)
            bd = re.sub(remove, "", bd)
            bd = re.sub('<br(\s+)?\/?>(\s+)?', " ", bd)  # 去掉<br >
            bd = re.sub('/', " ", bd)  # 替换/
            # data.append(bd.strip())
            # print(bd)
            words = bd.split('   ')
            for s1 in words:
                s2 = s1.split('   ')
                for s3 in s2:
                    if len(s3) != 0 and s3 != " ":  #
                        # print("s3 = " + s3)
                        # if s3.startswith("主演"):
                            # print("s3 = " + s3)
                            # print("s3[0:-5]=" + s3[0:-5])
                            # print("s3[-4:]=" + s3[-4:])
                        if (s3[-4:].isdigit()):
                        # if s3.startswith("主演"):
                            data.append(s3[0:-5])
                            data.append(s3[-4:])
                        elif s3.endswith(")"):
                            data.append(s3[0:-11])
                            data.append(s3[-10:])
                        else:
                            data.append(s3)
            # 主演有可能因为导演内容太长而没有
            # print(len(data))
            if (len(data) != 12):
                data.insert(8, ' ')  # 留空
            datalist.append(data)
    return datalist

# 保存数据
def saveData(datalist, savePath):
    book = xlwt.Workbook(encoding="utf-8", style_compression=0)
    sheet = book.add_sheet('豆瓣电影Top250', cell_overwrite_ok=True)
    col = ('电影详情链接', '图片链接', '影片中文名', '影片外国名', '评分', '评价数', '概况', '导演', '主演', '年份', '国家', '类别')
    for i in range(0, 12):
        sheet.write(0, i, col[i])
    for i in range(0, 250):
        data = datalist[i]
        for j in range(0, 12):
            sheet.write(i + 1, j, data[j])
    book.save(savePath)


def main():
    print("开始爬取...")
    baseurl = "https://movie.douban.com/top250?start="
    datalist = getData(baseurl)  # 获取数据
    savePath = "C:\\Users\\lenovo\\Documents\\data\\豆瓣电影Top250.xls"
    saveData(datalist, savePath)  # 保存数据


if __name__ == '__main__':
    main()
    print("爬取完成，请查看.xls文件")
