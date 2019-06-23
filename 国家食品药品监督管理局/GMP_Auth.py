# -*- coding: utf-8 -*-
from selenium import webdriver
from bs4 import BeautifulSoup
import time
from pymongo import MongoClient
#from zhimaip import getdailione


# 连接mongodb数据库
def connect_db():
    # 建立MongoDB数据库连接
    client = MongoClient('127.0.0.1', 25000)
    # 用户验证
    db = client.raw
    db.authenticate("raw", "raw_bigdata963qaz")
    # 连接所用集合，也就是我们通常所说的表
    collection = db.drugs_GMP_Auth
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
          'tableId=23&tableName=TABLE23&tableView=GMP认证&Id=' + str(id)  # GMP认证详情地址
    # ascp = driver.execute_script('return oldContent')  # 解析html中js代码
    # soup = BeautifulSoup(ascp[0], 'lxml')
    try:
        driver.get(url)
        soup = BeautifulSoup(driver.page_source)
        if '没有相关信息' in driver.page_source:
            print(str(id) + '：没有该详情页面')
        else:
            trs = soup.find('div', {'class': 'listmain'}).find('div').find_all('table')[0].find('tbody').find_all('tr')
            # 插入数据库
            coll.insert({
                # 企业列表id号（详情id）
                'detail_id': id,
                # 省市
                'province': trs[1].find_all('td')[1].text.strip(),
                # 证书编号
                'cerific_number': trs[2].find_all('td')[1].text.strip(),
                # 企业名称
                'company_name': trs[3].find_all('td')[1].text.strip(),
                # 地址
                'address': trs[4].find_all('td')[1].text.strip(),
                # 认证范围
                'auth_range': trs[5].find_all('td')[1].text.strip(),
                # 发证日期
                'send_cerific_date': trs[6].find_all('td')[1].text.strip(),
                # 有效期截止日
                'effective_date': trs[7].find_all('td')[1].text.strip(),
                # 批准延续日期
                'approve_conti_date': trs[8].find_all('td')[1].text.strip(),
                # 有效期延续至
                'effective_conti_date': trs[9].find_all('td')[1].text.strip(),
                # 批准延续的认证范围
                'approve_conti_cerific_date': trs[10].find_all('td')[1].text.strip(),
                # 认证GMP版本
                'cerific_gmp_version': trs[11].find_all('td')[1].text.strip(),
                # 备注
                'remakes': trs[12].find_all('td')[1].text.strip(),
                # 注
                'notes': trs[14].find_all('td')[1].text.strip(),
                # 爬取时间
                'crawl_time': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            })
    except Exception as e:
        print(e, id)
        detail_data(id)


if __name__ == "__main__":
    coll = connect_db()     # 得到数据库连接
    driver = driver()   # 模拟浏览器

    # 循环详情页浏览器模拟
    for id in range(721,722):
        try:
            detail_data(id)
        except Exception as e:
            print(e, id)
            detail_data(id)
    driver.quit()
    driver.close()

