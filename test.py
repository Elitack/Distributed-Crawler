
from Manager.ProxyManager import ProxyManager
from Scheduler.ProxyValidSchedule import run as ValidRun
from multiprocessing import Process
import time
import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.proxy import ProxyType
import requests


dcap = dict(DesiredCapabilities.PHANTOMJS)  # 设置userAgent

#使用移动端浏览器ua
dcap["phantomjs.page.settings.userAgent"] = ("Mozilla/5.0 (Linux; Android 5.1.1; Nexus 6 Build/LYZ28E) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.23 Mobile Safari/537.36")


print("start")
obj = webdriver.PhantomJS(executable_path="/home/jack/Downloads/App/phantomjs-2.1.1-linux-x86_64/bin/phantomjs", desired_capabilities=dcap)
obj.maximize_window()
obj.get("http://www.tianyancha.com/")
obj.get_screenshot_as_file("/home/jack/Documents/test2.png")
print ("tianyancha done")
proxy = webdriver.Proxy()
proxy.proxy_type = ProxyType.MANUAL
proxy.http_proxy = "175.169.131.123:8118"
proxy.add_to_capabilities(webdriver.DesiredCapabilities.PHANTOMJS)
obj.start_session(webdriver.DesiredCapabilities.PHANTOMJS)


r = requests.get('http://www.tianyancha.com/', proxies={"http" : "http://175.169.131.123:8118"}, timeout=5, verify=False)
print (r.status_code)
obj.get("http://www.tianyancha.com/")
print (obj.page_source)
obj.get_screenshot_as_file("/home/jack/Documents/test.png")