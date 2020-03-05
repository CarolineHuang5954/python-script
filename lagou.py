# coding=utf-8

import random
import time

import requests
from openpyxl import Workbook
import pymysql.cursors


def get_conn():
    '''建立数据库连接'''
    conn = pymysql.connect(host='localhost',
                           user='root',
                           password='root',
                           db='python',
                           charset='utf8mb4',
                           cursorclass=pymysql.cursors.DictCursor)
    return conn


def insert(conn, info):
    '''数据写入数据库'''
    with conn.cursor() as cursor:
        sql = "INSERT INTO `python` (`shortname`, `fullname`, `industryfield`, `companySize`, `salary`, `city`, `education`) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, info)
    conn.commit()


def get_json(page, lang_name):
    # 主url
    url1 = 'https://www.lagou.com/jobs/list_python?city=%E5%85%A8%E5%9B%BD&cl=false&fromSearch=true&labelWords=&suginput='
    # ajax请求
    url = "https://www.lagou.com/jobs/positionAjax.json?px=default&needAddtionalResult=false"
    # url = 'https://www.lagou.com/jobs/positionAjax.json?city={}&needAddtionalResult=false'.format(i)
    '''返回当前页面的信息列表'''
    # headers = {
    #     'Host': 'www.lagou.com',
    #     'Connection': 'keep-alive',
    #     'Content-Length': '23',
    #     'Origin': 'https://www.lagou.com',
    #     'X-Anit-Forge-Code': '0',
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0',
    #     'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    #     'Accept': 'application/json, text/javascript, */*; q=0.01',
    #     'X-Requested-With': 'XMLHttpRequest',
    #     'X-Anit-Forge-Token': 'None',
    #     'Referer': 'https://www.lagou.com/jobs/list_%E8%BF%90%E7%BB%B4?city=%E6%88%90%E9%83%BD&cl=false&fromSearch=true&labelWords=&suginput=',
    #     'Accept-Encoding': 'gzip, deflate, br',
    #     'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7'
    # }
    #下面这个headers可以
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Referer': 'https://www.lagou.com/jobs/list_%E8%BF%90%E7%BB%B4?city=%E6%88%90%E9%83%BD&cl=false&fromSearch=true&labelWords=&suginput=',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
    }
    s = requests.Session()  # 建立session
    s.get(url=url1, headers=headers, timeout=3)
    cookie = s.cookies  # 获取cookie
    print(cookie)
    data = {'first': 'false', 'pn': page, 'kd': lang_name}
    json = s.post(url=url, data=data, headers=headers, cookies=cookie,timeout=3).json()
    time.sleep(7)
    print(json)
    list_con = json['content']['positionResult']['result']
    info_list = []
    for i in list_con:
        info = []
        info.append(i.get('companyShortName', '无'))
        info.append(i.get('companyFullName', '无'))
        info.append(i.get('industryField', '无'))
        info.append(i.get('companySize', '无'))
        info.append(i.get('salary', '无'))
        info.append(i.get('city', '无'))
        info.append(i.get('education', '无'))
        info_list.append(info)
    return info_list


def main():
    lang_name = 'python'
    wb = Workbook()  # 打开 excel 工作簿
    conn = get_conn()  # 建立数据库连接  不存数据库 注释此行
    # for i in ['北京', '上海', '广州', '深圳', '杭州']:  # 五个城市
    for i in ['天津']:  # 五个城市
        page = 1
        ws1 = wb.active
        ws1.title = lang_name

        while page < 31:  # 每个城市30页信息
            info = get_json(page, lang_name)
            if info is None:
                return
            page += 1
            print(i, 'page', page)
            time.sleep(random.randint(10, 20))
            print(info)
            for row in info:
                insert(conn, tuple(row))  # 插入数据库，若不想存入 注释此行
                ws1.append(row)
    conn.close()  # 关闭数据库连接，不存数据库 注释此行
    wb.save('{}职位信息.xlsx'.format(lang_name))


if __name__ == '__main__':
    main()
