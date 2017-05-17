# -*- coding:utf-8 -*-
import time
import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.proxy import ProxyType

import sys
from multiprocessing import Process

sys.path.append('../')

from Scheduler.ProxyValidSchedule import run as ValidRun
from Scheduler.ProxyRefreshScheduler import run as RefreshRun

from Manager.ProxyManager import ProxyManager

#fun：查找公司
def find_com(driver, company):
    driver.find_element_by_xpath("//*[@id='ng-view']/div[1]/div/div[2]/form/input").send_keys(Keys.TAB)
    driver.find_element_by_xpath("//*[@id='ng-view']/div[1]/div/div[2]/form/input").clear()
    driver.find_element_by_xpath("//*[@id='ng-view']/div[1]/div/div[2]/form/input").send_keys(company)
    driver.find_element_by_xpath("//*[@id='ng-view']/div[1]/div/div[2]/div").click()
    time.sleep(3)
    try:
        driver.find_element_by_xpath("//*[@id='ng-view']/div[2]/div/div/div/div[4]/div[1]/div[1]/div[1]/a/span[1]").click()  # 点击第一条
    except:
        driver.find_element_by_xpath("//*[@id='ng-view']/div[2]/div/div/div/div[3]/div[1]/div[1]/div[1]/a/span[1]").click()
    time.sleep(4)
    try:
        driver.find_element_by_xpath("//*[@id='ng-view']/div[2]/div[6]/div[13]/span[2]/a").click()  # 展开经营范围详细信息
    except:
        pass

#fun：第一次搜索
def first_com(driver, company):
    driver.get("http://www.tianyancha.com/")
    time.sleep(2)
    driver.find_element_by_xpath("//*[@id='ng-view']/div/div[1]/div[2]/div/form/input").send_keys(Keys.TAB)
    driver.find_element_by_xpath("//*[@id='ng-view']/div/div[1]/div[2]/div/form/input").send_keys(company)
    driver.find_element_by_xpath("//*[@id='ng-view']/div/div[1]/div[2]/div/div").click()  # 点击搜索
    time.sleep(3)
    driver.find_element_by_xpath("//*[@id='ng-view']/div[2]/div/div/div/div[4]/div[1]/div[1]/div[1]/a/span[1]").click()  # 点击第一条
    time.sleep(2)
    with open("result.csv", 'a', newline="", encoding='utf-8') as datacsv:
        csvwriter = csv.writer(datacsv)
        csvwriter.writerow(['公司名称', '组织机构代码 ', '工商注册号 ', '法定代表人 ', '注册资本 ', '注册地址 ', '注册时间 ', '登记机关 ', '企业类型 ', '核准日期 ', '状态', '营业期限 ', '行业 ', '经营范围'])

#fun：后退
def back(driver):
    driver.back()
    time.sleep(3)

#fun：公司页面检索信息
def cp_info(driver):
    com_name = driver.find_element_by_xpath("//*[@id='ng-view']/div[2]/div[1]/div[1]/div[1]").text     #company name
    try:
        org_id = driver.find_element_by_xpath("//*[@id='ng-view']/div[2]/div[6]/div[8]/span[2]").text  # 组织机构代码
    except:
        org_id = "未公开"

    try:
        reg_id = driver.find_element_by_xpath("//*[@id='ng-view']/div[2]/div[6]/div[7]/span[2]").text  # 工商注册号
    except:
        reg_id = "未公开"

        # credit_id = driver.find_element_by_xpath("").text      #统一信用代码
    try:
        legal_person = driver.find_element_by_xpath("//*[@id='ng-view']/div[2]/div[6]/div[1]/a").text  # 法定代表人
    except:
        legal_person = "未公开"

    try:
        reg_capital = driver.find_element_by_xpath("//*[@id='ng-view']/div[2]/div[6]/div[4]/span[2]").text  # 注册资本
    except:
        reg_capital = "未公开"

    try:
        reg_address = driver.find_element_by_xpath("//*[@id='ng-view']/div[2]/div[6]/div[12]/span[2]").text  # 注册地址
    except:
        reg_address = "未公开"

    try:
        reg_time = driver.find_element_by_xpath("//*[@id='ng-view']/div[2]/div[6]/div[3]/span[2]").text  # 注册时间
    except:
        reg_time = "未公开"

    try:
        reg_institution = driver.find_element_by_xpath("//*[@id='ng-view']/div[2]/div[6]/div[11]/span[2]").text  # 登记机关
    except:
        reg_institution = "未公开"

    try:
        enterprise_type = driver.find_element_by_xpath("//*[@id='ng-view']/div[2]/div[6]/div[6]/span[2]").text  # 企业类型
    except:
        enterprise_type = "未公开"

    try:
        issue_time = driver.find_element_by_xpath("//*[@id='ng-view']/div[2]/div[6]/div[10]/span[2]").text  # 核准日期
    except:
        issue_time = "未公开"

    try:
        business_status = driver.find_element_by_xpath("//*[@id='ng-view']/div[2]/div[6]/div[2]/span[2]").text  # 状态
    except:
        business_status = "未公开"

    try:
        business_term = driver.find_element_by_xpath("//*[@id='ng-view']/div[2]/div[6]/div[9]/span[2]").text  # 营业期限
    except:
        business_term = "未公开"

    try:
        business_type = driver.find_element_by_xpath("//*[@id='ng-view']/div[2]/div[6]/div[5]/span[2]").text  # 行业
    except:
        business_type = "未公开"

    try:
        business_scope = driver.find_element_by_xpath("//*[@id='ng-view']/div[2]/div[6]/div[13]/span[2]/span").text  # 经营范围
    except:
        business_scope = "未公开"

    with open("result.csv", 'a', newline="", encoding='utf-8') as datacsv:                 #记录到csv文件
        csvwriter = csv.writer(datacsv)
        csvwriter.writerow([com_name, org_id, reg_id, legal_person, reg_capital, reg_address, reg_time, reg_institution, enterprise_type, issue_time, business_status, business_term, business_type, business_scope])

p_list = list()
p1 = Process(target=ValidRun, name='ValidRun')
p_list.append(p1)
p2 = Process(target=RefreshRun, name='RefreshRun')
p_list.append(p2)
for p in p_list:
    p.start()

pm = ProxyManager()
pm.refresh()
print (pm.getNum())


dcap = dict(DesiredCapabilities.PHANTOMJS)  # 设置userAgent

#使用移动端浏览器ua
dcap["phantomjs.page.settings.userAgent"] = ("Mozilla/5.0 (Linux; Android 5.1.1; Nexus 6 Build/LYZ28E) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.23 Mobile Safari/537.36")



obj = webdriver.PhantomJS(executable_path="/home/jack/Downloads/App/phantomjs-2.1.1-linux-x86_64/bin/phantomjs", desired_capabilities=dcap)
obj.maximize_window()

#初始化搜索
first_com(obj, u"初始化")

company = open("../web_ch.txt", 'r', encoding='gbk')
line = company.readline()

i=0


while line:
    try:
        i=i+1

        print ("ip done")
        print("start crawling")
        flag = str(i)
        print("searching "+flag+" ...................")
        re_com = line.strip('\n')
        line = company.readline()
        proxy = webdriver.Proxy()
        proxy.proxy_type = ProxyType.MANUAL
        proxy.http_proxy = pm.get().decode("utf-8").strip("https://").strip("http://")
        print (proxy.http_proxy)
        proxy.add_to_capabilities(webdriver.DesiredCapabilities.PHANTOMJS)
        obj.start_session(webdriver.DesiredCapabilities.PHANTOMJS)
        obj.get("http://www.tianyancha.com/")         #后退
        time.sleep(5)
        find_com(obj, re_com)       #查找
        cp_info(obj)         #记录
    except Exception as err:
        print (err)
        print (obj.page_source)









###########################################
### pc端代码（反爬） ###
# import time
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
#
# dcap = dict(DesiredCapabilities.PHANTOMJS)  # 设置userAgent
# dcap["phantomjs.page.settings.userAgent"] = ("Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36")
#
# obj = webdriver.PhantomJS(executable_path=r"C:\Users\hjw99868\Desktop\phantomjs-1.9.7-windows\phantomjs.exe", desired_capabilities=dcap)
# obj.maximize_window()
# obj.get('http://www.tianyancha.com/')
#
# obj.find_element_by_id('live-search').send_keys(Keys.TAB)
# obj.find_element_by_id('live-search').send_keys('百度')
# obj.find_element_by_css_selector('div.input-group-addon.search_button > span').click()
# time.sleep(2)
# #标签页切换
# handle = obj.current_window_handle
# obj.find_element_by_xpath("//*[@id='ng-view']/div[2]/div/div/div[1]/div[3]/div[1]/div[2]/div[1]/div[1]/a/span").click()
# handles = obj.window_handles
# for newhandle in handles:
#     if newhandle != handle:
#         obj.switch_to_window(newhandle)
# print(obj.page_source)
# obj.get_screenshot_as_file('bai.png')
###############################################

###############################################
### 测试是否有验证码 ###
# for i in range(150041670,150041700):
#     ip = str(i)
#     url = 'http://www.tianyancha.com/company/' + ip
#     obj.get(url)
#     test = obj.find_element_by_xpath("//*[@id='ng-view']/div[2]/div[1]/div[1]/div[1]").text
#     if test == '很抱歉，您要访问的页面不存在':
#         print(ip)
#     else:
#         print(test)
# obj.get_screenshot_as_file("123.png")
###############################################



