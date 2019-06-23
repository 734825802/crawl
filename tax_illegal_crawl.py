# -*- coding: utf-8 -*-
import requests
from selenium import webdriver
from  bs4 import BeautifulSoup
from zhimaip import getdailione
from pymongo import MongoClient
import time
import logging
import sys

def connect_mongo_db():
    try:
        # 建立连接
        mongo_clinet = MongoClient('127.0.0.1', 25000)
        # 连接数据库
        db = mongo_clinet.raw
        # 用户验证
        db.authenticate('raw', 'raw_bigdata963qaz')
        # 连接集合，也就是mongodb数据库表
        collection = db.tax_illegal_case
        return mongo_clinet, collection
    except Exception as e:
        logging.error(e)

# 浏览器模拟
def driver():
    #ip,exttime = getdailione(5)           # 调用芝麻IP
    # 模拟浏览器
    # ip = 'http://47.98.220.20:16800'
    ip = 'http://129.211.36.69:9001'
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--proxy-server=' + ip)
    driver = webdriver.Chrome(chrome_options=chrome_options)  # 加载浏览器驱动
    # driver.maximize_window() #窗口最大化
    return driver

def detail_data(month):
    try:
        url = "http://hd.chinatax.gov.cn/xxk/action/ListXinxikucomXml.do?dotype=casetime&id=" + month
        print(url)
        driver.get(url)
        time.sleep(2)
        soup = BeautifulSoup(driver.page_source, 'lxml')
        line_list = soup.find('div', {'class': 'collapsible-content'}).find_all('div', {'class': 'line'})
        for line in line_list:
            detail_id = line.find_all('span', {'class': 'html-attribute-value'})[0].text.strip()
            # company_name = line.find_all('span', {'class': 'html-attribute-value'})[1].text.strip()
            url1 = 'http://hd.chinatax.gov.cn/xxk/action/GetArticleView1.do?op=xxkweb&id=' + detail_id
            if not collection.find_one({'detail_id': detail_id}):
                driver.get(url1)
                time.sleep(2)
                soup1 = BeautifulSoup(driver.page_source, 'lxml')
                tr_list = soup1.find_all('table')[1].find_all('tr')
                if len(tr_list) == 9:
                    # 插入数据库
                    collection.insert({
                        # 公司名称（纳税人姓名）
                        'company_name': tr_list[0].find_all('td')[1].text.strip(),
                        # 纳税人识别号
                        'id_tax': tr_list[1].find_all('td')[1].text.strip(),
                        # 组织机构代码
                        'org_code': tr_list[2].find_all('td')[1].text.strip(),
                        # 注册地址
                        'reg_address': tr_list[3].find_all('td')[1].text.strip(),
                        # 法定代表人或者负责人姓名、性别、证件名称及号码
                        'legal_person': tr_list[4].find_all('td')[1].text.strip(),
                        # 负有直接责任的财务负责人姓名、性别、证件名称及号码
                        'direct': tr_list[5].find_all('td')[1].text.strip(),
                        # 负有直接责任的中介机构信息及其从业人员信息
                        'gency_info': tr_list[6].find_all('td')[1].text.strip(),
                        # 案件性质
                        'cases_nature': tr_list[7].find_all('td')[1].text.strip(),
                        # 主要违法事实，相关法律依据及税务处理处罚情况
                        'illegal_facts': tr_list[8].find_all('td')[1].text.strip(),
                        'state': '公司',
                        'detail_id': detail_id,
                        'year': year,
                        'month': month,
                        'crawl_time': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                    })
                else:
                    collection.insert({
                        # 姓名
                        'name': tr_list[0].find_all('td')[1].text.strip(),
                        # 性别
                        'sex': tr_list[1].find_all('td')[1].text.strip(),
                        # 证件名称及号码
                        'id_card': tr_list[2].find_all('td')[1].text.strip(),
                        # 负有直接责任的中介机构信息及其从业人员信息
                        'gency_info': tr_list[3].find_all('td')[1].text.strip(),
                        # 案件性质
                        'cases_nature': tr_list[4].find_all('td')[1].text.strip(),
                        # 主要违法事实  相关法律依据及税务处理处罚情况
                        'illegal_facts': tr_list[5].find_all('td')[1].text.strip(),
                        'state': "个人",
                        'detail_id': detail_id,
                        'year': year,
                        'month': month,
                        'crawl_time': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                    })
    except Exception as e:
        print(e, month)
        detail_data(month)


if __name__ == "__main__":
    # 设置打印日志信息级别
    logging.basicConfig(format='%(asctime)s - %(pathname)s[line:%(lineno)d]-%(levelname)s:%(message)s',
                        level=logging.DEBUG)
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)

    # 连接MongoDB数据库
    client, collection = connect_mongo_db()
    driver = driver()  # 模拟浏览器
    date = {
        '2014': ['2014年4季度'],
        '2015': ['2015年2季度', '2015年3季度', '2015年4季度'],
        '2016': ['2016年1季度', '2016年2季度', '2016年3季度', '2016年10月', '2016年11月', '2016年12月'],
        '2017': ['2017年1月', '2017年2月', '2017年3月', '2017年5月', '2017年6月', '2017年7月', '2017年8月', '2017年9月',
                 '2017年10月', '2017年11月', '2017年12月'],
        '2018': ['2018年1月', '2018年2月', '2018年3月', '2018年4月', '2018年5月', '2018年6月', '2018年7月', '2018年8月',
                 '2018年9月', '2018年10月', '2018年11月', '2018年12月'],
        '2019': ['2019年1月', '2019年2月', '2019年3月', '2019年4月']
    }
    for year in date:
        for month in date[year]:
            try:
                detail_data(month)
            except Exception as e:
                print(e, month)
                detail_data(month)

    driver.close()
    client.close()
