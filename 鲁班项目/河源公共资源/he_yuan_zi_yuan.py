# -*-coding: utf-8 -*-
from pymongo import MongoClient
import requests
from bs4 import BeautifulSoup
import time
import datetime

# 连接mongodb数据库
def connect_db():
    try:
        # 建立MongoDB数据库连接
        # client = MongoClient('127.0.0.1', 25000)
        client = MongoClient('192.168.111.210', 27017)

        # 用户验证
        # db = client.raw
        # db.authenticate("raw", "raw_bigdata963qaz")

        # 连接数据库
        db = client.luban
        # 连接所用集合，也就是我们通常所说的表
        collection = db.meizhou_heyuan_shaoguan
        return collection, client
    except Exception as e:
        print(e)

# 从标题中清分出区域
def get_area(title):
    if title.find('省') > -1 and (title.find('区') > -1 or title.find('县') > - 1):
        area = title[title.find('省') + 1: (title.find('区') + 1 or title.find('县') + 1)]
    elif title.find('市') > -1 and (title.find('区') > -1 or title.find('县') > - 1):
        area = title[title.find('市') + 1: (title.find('区') + 1 or title.find('县') + 1)]
    elif title.find('市') > -1:
        area = title[:title.find('市') + 1]
    elif title.find('区') > -1 and title.find('县') > - 1:
        if title.find('区') > title.find('县') and title.find('县') + 1 == title.find('区'):
            area = title[:title.find('区') + 1]
        else:
            area = title[:title.find('县') + 1]
    elif title.find('区') > -1:
        area = title[:title.find('区') + 1]
    elif title.find('县') > -1:
        area = title[:title.find('县') + 1]
    else:
        area = ''
    return area

# 翻页
def page_down(page):
    page += 1
    if page == 1:
        page = 'subpage'
    type_dict = {
        '政府采购': {
            '采购公告': 'http://61.143.150.176/zfcg/' + str(page) + '.html',
        },
        '建设工程': {
            '交易公告': 'http://61.143.150.176/jsgc/' + str(page) + '.html'
        },
        '土矿交易': {
            '交易公告': 'http://61.143.150.176/tdhkcjy/' + str(page) + '.html'
        },
        '产权交易': {
            '交易公告': 'http://61.143.150.176/cqjy/' + str(page) + '.html'
        }
    }
    # 对每个类型进行循环遍历
    for (trade_info, v) in type_dict.items():   # 对交易信息遍历
        for (trade_type, url) in v.items():     # 对交易类型遍历
            detail_data(trade_info, trade_type, url, page)

"""
trade_type：交易类型
url：交易类型请求地址
page: 请求翻页
"""
def detail_data(trade_info, trade_type, url, page):
    try:
        res = requests.get(url, headers=headers, proxies=proxies)
        res.encoding = res.apparent_encoding
        soup = BeautifulSoup(res.text, 'lxml')
        li_list = soup.find('div', {'class': 'ewb-list-bd'}).find('ul').find_all('li')
        for i in range(len(li_list)):
            pub_date = li_list[i].find('span', {'class': 'r'}).text.strip()  # 公告日期
            if pub_date != day:
                flag = False
                break
            else:
                flag = True
                title = li_list[i].find('a', attrs={'title': True}).attrs['title']  # 标题
                href = li_list[i].find('a', attrs={'href': True}).attrs['href']  # 标签链接
                detail_url = 'http://61.143.150.176' + href  # 详情页面链接
                if not coll.find_one({'detail_url': detail_url}):
                    if li_list[i].find('a').find_all('font'):
                        area = li_list[i].find('a').find_all('font')[0].text.strip()[1:-1]  # 地区
                        trade_type = li_list[i].find('a').find_all('font')[1].text.strip()[1:-1]  # 交易类型
                    else:
                        area = get_area(title)
                    response = requests.get(detail_url, headers=headers, proxies=proxies)
                    response.encoding = response.apparent_encoding
                    html = response.text
                    coll.insert({
                        # 交易信息
                        'trade_info': trade_info,
                        # 交易类型
                        'trade_type': trade_type,
                        'province': '广东省',
                        'city': '河源市',
                        'area': area,
                        # 标题
                        'title': title,
                        # 公告日期
                        'pub_date': pub_date,
                        # 详情页面链接
                        'detail_url': detail_url,
                        # 网站名称
                        'website': '河源市公共资源',
                        # 内容
                        'html': html,
                        'crawl_time': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                    })
                    print(detail_url)
        if flag:
            if page == 'subpage':
                page = 1
                page_down(page)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    # 获取当前日期时间
    day = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    # now_time = datetime.datetime.now()
    # yes_time = now_time + datetime.timedelta(days=-1)  # 昨天日期时间
    # day = yes_time.strftime('%Y-%m-%d')  #格式化昨天日期

    # 连接Mongodb
    coll, client = connect_db()
    # 设置请求头
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN, zh;q=0.9',
        'Connection': 'keep-alive',
        'Host': '61.143.150.176',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla / 5.0(Windows NT 6.1; WOW64) AppleWebKit/537.36(KHTML, likeGecko) Chrome/75.0.3770.100 Safari/537.36'
    }
    proxies = {"https": "https://47.98.220.20:16800", "http": "http://47.98.220.20:16800"}  # 设置代理ip
    try:
        page_down(0)   # 调用页面请求函数
    except Exception as e:
        print(e)
    client.close()  # 关闭数据库连接
