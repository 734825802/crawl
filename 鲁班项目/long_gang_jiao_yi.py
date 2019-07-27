# -*-coding: utf-8 -*-
from pymongo import MongoClient
import requests
from bs4 import BeautifulSoup
import time
import json

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
        coll1 = db.long_gang_bid_bulletin       # 招标公告
        coll2= db.long_gang_bid_result          # 中标结果
        coll3 = db.long_gang_change_record      # 变更备案
        return coll1, coll2, coll3, client
    except Exception as e:
        print(e)

# 招标公告
def bid_bulletin(page):
    url = 'https://www.szjsjy.com.cn:8001/jyw-lg/lgjyxx/zbGongGaoList.do'  # 招标公告
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Host': 'www.szjsjy.com.cn:8001',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
    }
    formdata = {
        'currentPage': str(page),
        'pageSize': '10',
        'bdBH': '',
        'bdName': '',
        'ggName': '',
        'jsdw': '',
        'ggStartTime': '',
        'ggEndTime': '',
    }
    res = requests.post(url, headers=headers, proxies=proxies, data=formdata)
    res.encoding = res.apparent_encoding
    soup = BeautifulSoup(res.text, 'lxml')
    tr_list = soup.find_all('table', {'class': 'table_00 table_breakline'})[1].find_all('tr')
    for tr in tr_list[1:]:
            pub_time = tr.find_all('td')[4].text.strip()            # 发布时间
            pub_day = pub_time[:10]             # 截取到天
            if day != pub_day:
                flag = False
                break
            else:
                href = tr.find_all('td')[1].find('a')['href']               # 公告详情链接
                bid_project_num = tr.find_all('td')[0].text.strip()         # 招标项目编号
                bulletin_name = tr.find_all('td')[1].text.strip()           # 公告名称
                bid_project_name = tr.find_all('td')[2].text.strip()        # 招标项目名称
                project_type = tr.find_all('td')[3].text.strip()            # 工程类型
                detail_url = 'https://www.szjsjy.com.cn:8001' + href
                if not coll1.find_one({'detail_url': detail_url}):
                    response = requests.get(detail_url)
                    response.encoding = response.apparent_encoding
                    html = response.text
                    coll1.insert({
                        'bid_project_num': bid_project_num,
                        'bulletin_name': bulletin_name,
                        'bid_project_name': bid_project_name,
                        'project_type': project_type,
                        'pub_time': pub_time,
                        'detail_url': detail_url,
                        'trade_type': '招标公告',
                        'province': '广东省',
                        'city': '深圳市',
                        'area': '龙岗区',
                        'html': pub_time,
                        'crawl_time': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                    })
                    print(detail_url)
    if flag:
        page_down(page)


# 中标结果
def bid_result(page):
    url = 'https://www.szjsjy.com.cn:8001/jyw-lg/lgjyxx/pub/winResult/gotoList.do'  # 中标结果
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Host': 'www.szjsjy.com.cn:8001',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
    }
    formdata = {
        'currentPage': str(page),
        'pageSize': '10',
        'bdBH': '',
        'bdName': '',
        'ggName': '',
        'jsdw': '',
        'ggStartTime': '',
        'ggEndTime': '',
    }
    res = requests.post(url, headers=headers, proxies=proxies, data=formdata)
    res.encoding = res.apparent_encoding
    soup = BeautifulSoup(res.text, 'lxml')
    tr_list = soup.find_all('table', {'class': 'table_00 table_breakline'})[1].find_all('tr')
    for tr in tr_list[1:]:
        pub_time = tr.find_all('td')[3].text.strip()  # 发布时间
        pub_day = pub_time[:10]  # 截取到天
        if day != pub_day:
            flag = False
            break
        else:
            detail_url = tr.find_all('td')[1].find('a')['href']  # 中标结果详情链接
            if not coll2.find_one({'detail_url': detail_url}):
                bid_secion_num = tr.find_all('td')[0].text.strip()  # 标段编号
                bid_secion_name = tr.find_all('td')[1].text.strip()  # 标段名称
                project_type = tr.find_all('td')[2].text.strip()  # 工程类型
                response = requests.get(detail_url, proxies=proxies)
                response.encoding = response.apparent_encoding
                html = response.text
                coll2.insert({
                    'bid_secion_num': bid_secion_num,
                    'bid_secion_name': bid_secion_name,
                    'project_type': project_type,
                    'pub_time': pub_time,
                    'detail_url': detail_url,
                    'trade_type': '中标结果',
                    'province': '广东省',
                    'city': '深圳市',
                    'area': '龙岗区',
                    'html': html,
                    'crawl_time': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                })
                print(detail_url)
    if flag:
        page_down(page)


# 变更备案
def changeRecord(page):
    url = 'http://zjj.sz.gov.cn/htjg/web/webService/getChangeList.json'
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'http://zjj.sz.gov.cn',
        'Referer': 'http://zjj.sz.gov.cn/htjg/web/changelist.jsp',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
    }
    formdata = {
    'limit': 10,
    'offset': (page-1)*10,
    'pageNumber': page,
    'projectName': '',
}
    get_change_record_list = requests.post(url, data=formdata, headers=headers, proxies=proxies)
    get_change_record_list = json.loads(get_change_record_list.text)
    for change_record_dict in get_change_record_list['rows']:
        if change_record_dict['status_time'] != day:
            flag = False
            break
        else:
            if not coll3.find_one({'apply_code': change_record_dict['apply_code']}):       # 受理编号
                change_record_dict['crawl_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                coll3.insert(change_record_dict)
                print(change_record_dict['apply_code'])
    if flag:
        page_down(page)

# 翻页
def page_down(page):
    page += 1
    bid_bulletin(page)
    bid_result(page)
    changeRecord(page)

if __name__ == "__main__":
    # 获取当前日期时间
    day = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    # 连接Mongodb
    coll1, coll2, coll3, client = connect_db()
    proxies = {"https": "https://47.98.220.20:16800", "http": "http://47.98.220.20:16800"}  # 设置代理ip
    try:
        page_down(0)            # 调用页面请求函数
    except Exception as e:
       print(e)
    client.close()
