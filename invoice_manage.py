# -*- coding: utf-8 -*-
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from bs4 import BeautifulSoup
import datetime


def sq_query():
    # 需要增加申请日期作为参数
    now_time = datetime.datetime.now()
    now_date = now_time.strftime('%Y-%m-%d')
    start_time = now_time + datetime.timedelta(days=-30)  # 昨天日期时间
    start_date = start_time.strftime('%Y-%m-%d')  # 格式化昨天日期

    # 点击 发票申请
    xzsq_action = driver.find_element_by_id('xzsq')
    ActionChains(driver).move_to_element(xzsq_action).click(xzsq_action).perform()
    # 点击进销项复选框
    sjlx_action0 = driver.find_elements_by_name('sjlx')[0]
    ActionChains(driver).move_to_element(sjlx_action0).click(sjlx_action0).perform()

    # 销项票
    sjlx_action1 = driver.find_elements_by_name('sjlx')[1]
    ActionChains(driver).move_to_element(sjlx_action1).click(sjlx_action1).perform()

    # 点击发票类型复选框
    fplx_action0 = driver.find_elements_by_name('fplx')[0]
    ActionChains(driver).move_to_element(fplx_action0).click(fplx_action0).perform()

    fplx_action1 = driver.find_elements_by_name('fplx')[1]
    ActionChains(driver).move_to_element(fplx_action1).click(fplx_action1).perform()

    fplx_action2 = driver.find_elements_by_name('fplx')[2]
    ActionChains(driver).move_to_element(fplx_action2).click(fplx_action2).perform()

    fplx_action3 = driver.find_elements_by_name('fplx')[3]
    ActionChains(driver).move_to_element(fplx_action3).click(fplx_action3).perform()

    fplx_action4 = driver.find_elements_by_name('fplx')[4]
    ActionChains(driver).move_to_element(fplx_action4).click(fplx_action4).perform()

    fplx_action5 = driver.find_elements_by_name('fplx')[5]
    ActionChains(driver).move_to_element(fplx_action5).click(fplx_action5).perform()

    fplx_action6 = driver.find_elements_by_name('fplx')[6]
    ActionChains(driver).move_to_element(fplx_action6).click(fplx_action6).perform()

    fplx_action7 = driver.find_elements_by_name('fplx')[7]
    ActionChains(driver).move_to_element(fplx_action7).click(fplx_action7).perform()

    # 开票日期
    kprqq_action = driver.find_element_by_id('kprqq')
    ActionChains(driver).move_to_element(kprqq_action).click(kprqq_action).send_keys(start_date).perform()

    kprqz_action = driver.find_element_by_id('kprqz')
    ActionChains(driver).move_to_element(kprqz_action).click(kprqz_action).send_keys(now_date).perform()

    # 设置解压密码
    driver.find_element_by_id('jymm').send_keys('123456')
    driver.find_element_by_id('jymmqr').send_keys('123456')
    # 申请完成
    driver.find_element_by_id('commitdata').click()


def query_down(downlist):
    # 下载发票
    for i in range(len(downlist)):
        count = downlist[i]['count']
        content = downlist[i]['content']
        xz_action = driver.find_elements_by_link_text('下载')[count]
        ActionChains(driver).move_to_element(xz_action).click(xz_action).perform()
        # driver.find_element_by_partial_link_text(content).click()
        close_action = driver.find_element_by_link_text('×')
        ActionChains(driver).move_to_element(close_action).click(close_action).perform()
    print('关闭完成')


def query_check():
    # 查看是否有查询记录，并返回
    # 需要增加第三种情况的判断
    # 需要增加查询日期作为参数
    statusout = 0
    downlist = []
    count = 0

    # 点击按钮查询
    xzsqcx_action = driver.find_element_by_id('xzsqcx')
    ActionChains(driver).move_to_element(xzsqcx_action).click(xzsqcx_action).perform()

    # 查询状态
    soup = BeautifulSoup(driver.page_source)
    table_id = soup.find('table', {'id': 'exampleFpgj'})
    tr_list = table_id.find_all('tr')
    if table_id.tbody.text.strip() != '未找到符合条件的记录':
        for i in range(1, len(tr_list)):
            td_list = tr_list[i].find_all('td')
            # 发票类型
            fplx = td_list[2].text.strip()
            # 进销项
            jxx = td_list[5].text.strip()
            content = jxx + '-' + fplx
            print(content)
            # 处理状态
            status = td_list[6].text.strip()
            # 是否符合下载条件
            xz = td_list[7].text.strip()
            if status == '处理完成' and xz == '下载':
                downlist.append({'count': count, 'content': content})
                count += 1
                statusout = 2

    else:
        statusout = 1
    return statusout, downlist



def do_in_page1():
    # 查询页面应该做什么
    status, downlist = query_check()
    driver.implicitly_wait(5)
    if status == 1:     # 未查询到记录
        sq_query(driver)
        return True
    elif status == 2:  # 查询到有下载记录
        query_down(downlist)
        return False
    else:
        return True


def to_page1(password):
    # 增值税发票综合服务平台（江西）,禁入查询页面
    url0 = 'https://fpdk.jiangxi.chinatax.gov.cn'
    driver.get(url0)
    driver.implicitly_wait(5)

    # 弹出的升级页面
    okButton = driver.find_element_by_id('okButton')
    okButton.click()
    driver.implicitly_wait(10)

    # 登陆页面 输入密码
    action = driver.find_element_by_id("password1")
    ActionChains(driver).move_to_element(action).click(action).send_keys(password).perform()
    driver.find_element_by_id('submit').click()
    driver.implicitly_wait(5)

    # 发票管理的发票下载下拉框
    action1 = driver.find_element_by_name('menu_fpgl')
    action2 = driver.find_elements_by_name('group_fpgl')[0]
    ActionChains(driver).move_to_element(action1).click(action2).perform()

    # # 点击下载
    # driver.find_elements_by_xpath('//a[@style="color: red"]')[0].click()
    # # 点击zip下载
    # driver.find_elements_by_xpath('//a[@style="color: red"]')[1].click()

def log_in_invoice(password):
    # 进入查询页面
    try:
        to_page1(password)
    except Exception as e:
        to_page1(password)
    while (do_in_page1()):
        time.sleep(30)



if __name__ == '__main__':
    password = '12345678'
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.implicitly_wait(5)
    driverx = log_in_invoice(password)
