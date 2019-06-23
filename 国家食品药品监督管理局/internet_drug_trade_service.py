# -*- coding: utf-8 -*-
from selenium import webdriver
from bs4 import BeautifulSoup
import time
from pymongo import MongoClient


# 连接mongodb数据库
def connect_db():
    # 建立MongoDB数据库连接
    client = MongoClient('127.0.0.1', 27017)
    # db = client.raw
    # 用户验证
    # db.authenticate("raw", "raw_bigdata963qaz")
    db = client.crawl  # 连接数据库
    # 连接所用集合，也就是我们通常所说的表
    collection = db.internet_drug_trade_service
    return collection

# 浏览器模拟
def driver():
    # ip,exttime = getdailione(5)           # 调用芝麻IP
    # 模拟浏览器
    #ip = 'http://47.98.220.20:16800'
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    #chrome_options.add_argument('--proxy-server=' + ip)
    driver = webdriver.Chrome(chrome_options=chrome_options)  # 加载浏览器驱动
    # driver.maximize_window() #窗口最大化
    return driver

def detail_data(id):
    url = 'http://app1.sfda.gov.cn/datasearchcnda/face3/content.jsp?' \
          'tableId=33&tableName=TABLE33&tableView=互联网药品交易服务&Id=' + str(id)
    try:
        driver.get(url)
        soup = BeautifulSoup(driver.page_source)
        if '没有相关信息' in driver.page_source:
            print(str(id) + '：没有该详情页面')
        else:
            trs = soup.find('div', {'class': 'listmain'}).find('div').find_all('table')[0].find('tbody').find_all('tr')
            # 插入数据库
            coll.insert({
                # 详情id号
                'detail_id': id,
                # 证书编号
                'license_num': trs[1].find_all('td')[1].text.strip(),
                # 公司名称
                'company_name': trs[2].find_all('td')[1].text.strip(),
                # 法定代表
                'legal_person': trs[3].find_all('td')[1].text.strip(),
                # 网站名称
                'website_name': trs[4].find_all('td')[1].text.strip(),
                # 服务范围
                'service_range': trs[5].find_all('td')[1].text.strip(),
                # 域名
                'domain': trs[6].find_all('td')[1].text.strip(),
                # ip地址
                'IP_address': trs[7].find_all('td')[1].text.strip(),
                # 发证日期
                'send_cerific_date': trs[8].find_all('td')[1].text.strip(),
                # 有效截止日期
                'effective_end_date': trs[9].find_all('td')[1].text.strip(),
                # 单位地址
                'address': trs[10].find_all('td')[1].text.strip(),
                # 邮编
                'postal_code': trs[11].find_all('td')[1].text.strip(),
                'crawl_time': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            })
            print(id)
    except Exception as e:
        print(e, id)
        detail_data(id)

if __name__ == "__main__":
    coll = connect_db()  # 得到数据库连接
    driver = driver()  # 模拟浏览器

    # 详情页浏览器模拟
    for id in range(1000):
        try:
            detail_data(id)
        except Exception as e:
            print(e, id)
            detail_data(id)
    driver.quit()
