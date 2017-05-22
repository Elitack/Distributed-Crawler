
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
pm = ProxyManager()
print (pm.getNum())
pm.refresh()
print (pm.getNum())
p1 = Process(target=ValidRun, name='ValidRun')
p1.start()
#print (pm.get())

p1.join()
