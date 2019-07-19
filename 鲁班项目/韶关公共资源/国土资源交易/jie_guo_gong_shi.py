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
    url = 'http://www.sgjyzx.com/businessAnnounceAction!frontBusinessAnnounceIframeList.do?businessAnnounce.announcetype=22'   # post表单请求地址
    res = requests.post(url, data=formdata,  headers=headers, proxies=proxies, timeout=3)
    res.encoding = res.apparent_encoding
    soup = BeautifulSoup(res.text, 'lxml')
    tr_list = soup.find('table', {'id': 'dataList'}).find_all('tr')
    for i in range(1, len(tr_list)):
        # 标题
        title = tr_list[i].find('a').text.strip()
        # 地区
        area = tr_list[i].find_all('td')[1].find('span').text.strip()[:-2]
        # 链接
        href = tr_list[i].find_all('td')[1].find('a', attrs={'href': True}).attrs['href']
        # 发布时间
        pub_date = tr_list[i].find_all('td')[2].text.strip()
        # 具体链接详情页面
        detail_url = 'http://www.sgjyzx.com' + href
        response = requests.get(detail_url, headers=headers, proxies=proxies)
        response.encoding = response.apparent_encoding
        html = response.text
        coll.insert({
            # 交易信息
            'trade_info': '国土资源交易',
            # 交易类型
            'trade_type': '结果公示',
            'province': '广东省',
            'city': '韶关市',
            'area': area,
            # 标题
            'title': title,
            # 公告日期
            'pub_date': pub_date,
            # 详情页面链接
            'href': detail_url,
            # 网站名称
            'website': '韶关市公共资源',
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
                  'Cache-Control':  'max-age=0',
                  'Connection': 'keep-alive',
                  'Host': 'www.sgjyzx.com',
                  'Origin': 'http://www.sgjyzx.com',
                  'Upgrade-Insecure-Requests': '1',
                  'User-Agent': 'Mozilla / 5.0(Windows NT 6.1; WOW64) AppleWebKit/537.36(KHTML, likeGecko) Chrome/75.0.3770.100 Safari/537.36'
    }   # 请求头处理
    proxies = {"https": "https://47.98.220.20:16800", "http": "http://47.98.220.20:16800"}   # 代理IP
    for page in range(1, 3):
        formdata = {
            'searchvalue': '',
            'businessAnnounce.dpId': '',
            'pageSize': '20',
            'page': str(page),
            'sortField': 'RELEASETIME',
            'sortOrder': 'DESC',
        }
        try:
            detail_data(page)
        except Exception as e:
            print(e, page)
            detail_data(page)
    client.close()