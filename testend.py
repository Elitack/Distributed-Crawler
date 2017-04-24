# coding = utf-8

import urllib.request
import urllib.parse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

import sys
import os
import re
import time
import _thread
import threading
from threadPool import Pool
from dao import SQL as DB

def mainWork():
	while True:
		print("a")
		time.sleep(1)

th = _thread.start_new_thread(mainWork,())


while True:
	time.sleep(6)
	th.exit(0)
	sys.exit(0)