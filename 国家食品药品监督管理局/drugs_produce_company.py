# -*- coding: utf-8 -*-
from selenium import webdriver
from bs4 import BeautifulSoup
import time
from pymongo import MongoClient


# 连接mongodb数据库
def connect_db():
    # 建立MongoDB数据库连接
    client = MongoClient('127.0.0.1', 25000)
    # 用户验证
    db = client.raw
    db.authenticate("raw", "raw_bigdata963qaz")
    # 连接所用集合，也就是我们通常所说的表
    collection = db.drugs_produce_company
    return collection


# 浏览器模拟
def driver():
    # ip,exttime = getdailione(5)           # 调用芝麻IP
    # 模拟浏览器
    ip = 'http://47.98.220.20:16800'
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--proxy-server=' + ip)
    driver = webdriver.Chrome(chrome_options=chrome_options)  # 加载浏览器驱动
    # driver.maximize_window() #窗口最大化
    return driver

def detail_data(id):
    url = 'http://app1.sfda.gov.cn/datasearch/face3/content.jsp?' \
          'tableId=34&tableName=TABLE34&tableView=药品生产企业&Id=' + str(id)
    try:
        driver.get(url)
        soup = BeautifulSoup(driver.page_source)
        if '没有相关信息' in driver.page_source:
            print(str(id) + '：没有该详情页面')
        else:
            trs = soup.find('div', {'class': 'listmain'}).find('div').find_all('table')[0].find('tbody').find_all('tr')
            # 插入数据库
            coll.insert({
                # 企业列表id号
                'detail_id': id,
                # 编号
                'number': trs[1].find_all('td')[1].text.strip(),
                # 社会信用代码/组织机构代码
                'social_credit_code': trs[2].find_all('td')[1].text.strip(),
                # 分类码
                'classific_code': trs[3].find_all('td')[1].text.strip(),
                # 省市
                'province': trs[4].find_all('td')[1].text.strip(),
                # 企业名称
                'company_name': trs[5].find_all('td')[1].text.strip(),
                # 法定代表人
                'legal_person': trs[6].find_all('td')[1].text.strip(),
                # 企业负责人
                'company_leader': trs[7].find_all('td')[1].text.strip(),
                # 质量负责人
                'qualifi_person': trs[8].find_all('td')[1].text.strip(),
                # 注册地址
                'register_address': trs[9].find_all('td')[1].text.strip(),
                # 生产地址
                'produce_address': trs[10].find_all('td')[1].text.strip(),
                # 生产范围
                'produce_range': trs[11].find_all('td')[1].text.strip(),
                # 发证日期
                'send_cerific_date': trs[12].find_all('td')[1].text.strip(),
                # 有效期至
                'effective_date': trs[13].find_all('td')[1].text.strip(),
                # 发证机关
                'send_cerific_ogn': trs[14].find_all('td')[1].text.strip(),
                # 签发人
                'signer': trs[15].find_all('td')[1].text.strip(),
                # 日常监管机构
                'daily_sup_manager_ogn': trs[16].find_all('td')[1].text.strip(),
                # 日常监管人员
                'daily_sup_manager_person': trs[17].find_all('td')[1].text.strip(),
                # 监督举报电话
                'sup_report_phone': trs[18].find_all('td')[1].text.strip(),
                # 备注
                'remakes': trs[19].find_all('td')[1].text.strip(),
                # 注
                'notes': trs[22].find_all('td')[1].text.strip(),
                # 爬取时间
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
    for id in range(20000):
        try:
            detail_data(id)
        except Exception as e:
            print(e, id)

    driver.quit()
    driver.close()
