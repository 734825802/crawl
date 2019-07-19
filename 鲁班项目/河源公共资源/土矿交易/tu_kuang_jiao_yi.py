# -*-coding: utf-8 -*-
from pymongo import MongoClient
import requests
from bs4 import BeautifulSoup
import time

# 连接mongodb数据库
def connect_db():
    # 建立MongoDB数据库连接
    client = MongoClient('127.0.0.1', 25000)
    # 用户验证
    db = client.raw
    db.authenticate("raw", "raw_bigdata963qaz")
    # 连接所用集合，也就是我们通常所说的表
    collection = db.luban_meizhou_ziyuan
    return collection, client

def detail_data(page):
    if page == 1:
        page = 'subpage'
    url = 'http://61.143.150.176/tdhkcjy/' + str(page) + '.html'
    res = requests.get(url, headers=headers, proxies=proxies)
    res.encoding = res.apparent_encoding
    soup = BeautifulSoup(res.text, 'lxml')
    li_list = soup.find('div', {'class': 'ewb-list-bd'}).find('ul').find_all('li')
    for i in range(len(li_list)):
        title = li_list[i].find('a', attrs={'title': True}).attrs['title']      # 标题
        if li_list[i].find('a').find_all('font'):
            area = li_list[i].find('a').find_all('font')[0].text.strip()[1:-1]      # 地区
            trade_type = li_list[i].find('a').find_all('font')[1].text.strip()[1:-1]  # 交易类型
        else:
            trade_type = ''       # 交易类型
            if title.find('省') > -1 and (title.find('区') > -1 or title.find('县') > - 1):
                area = title[title.find('省') + 1: (title.find('区') + 1 or title.find('县') + 1)]
            elif title.find('市') > -1 and (title.find('区') > -1 or title.find('县') > - 1):
                area = title[title.find('市') + 1: (title.find('区') + 1 or title.find('县') + 1)]
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
        href = li_list[i].find('a', attrs={'href': True}).attrs['href']         # 标签链接
        pub_date = li_list[i].find('span', {'class': 'r'}).text.strip()         # 公告日期
        detail_url = 'http://61.143.150.176' + href                      # 详情页面链接
        response = requests.get(detail_url, headers=headers, proxies=proxies)
        response.encoding = response.apparent_encoding
        html = response.text
        coll.insert({
            # 交易信息
            'trade_info': '土矿交易',
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
            'href': detail_url,
            # 网站名称
            'website': '河源市公共资源',
            # 内容
            'html': html,
            'crawl_time': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        })


if __name__ == "__main__":
    coll, client = connect_db()     # 得到数据库连接
    headers = {
                  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
                  'Accept-Encoding': 'gzip, deflate',
                  'Accept-Language': 'zh-CN,zh;q=0.9',
                  'Connection': 'keep-alive',
                  'Host': '61.143.150.176',
                  'Upgrade-Insecure-Requests': '1',
                  'User-Agent': 'Mozilla / 5.0(Windows NT 6.1; WOW64) AppleWebKit/537.36(KHTML, likeGecko) Chrome/75.0.3770.100 Safari/537.36'
    }
    proxies = {"https": "https://47.98.220.20:16800", "http": "http://47.98.220.20:16800"}
    for page in range(1, 3):
        try:
            detail_data(page)
        except Exception as e:
            print(e, page)
            detail_data(page)
    client.close()