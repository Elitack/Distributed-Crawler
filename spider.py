# coding = utf-8

import urllib.request
import urllib.parse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

import sys
import os
import signal
import re
import time
import threading
from threadPool import Pool
from dao import SQL as DB


ip = ""
mode = "run"
if len(sys.argv) > 1: mode = sys.argv[1]
if len(sys.argv) > 2:   ip = sys.argv[2]
print("mode:", mode)
print("proxy:", ip)

delay = 3
layout = 0
retcount = 0
overcount = 0
lock = threading.Lock()
DEBUG = True

def debug(*args):
	if DEBUG:
		print(*args)
def info(*args, layout = 0):
	print("%25s"%ip,'|'+(' '*25+'|')*layout, *args, flush = True)

class Spider:
	def __init__(self,layout):
		self.layout = layout
		# self.db = DB()
		service_args = [
		    '--proxy='+ip,
		    '--proxy-type=http',
		    ]
		# print(ip)
		self.driver = webdriver.PhantomJS(executable_path = './phantomjs2.1.1/bin/phantomjs.exe', service_args = service_args)
		# info("init driver", layout = self.layout)
		self.getpage = re.compile("共([0-9]+)页")
		self.getcid = re.compile("http://www.tianyancha.com/company/([0-9]*)")
	def __del__(self):
		try:
			if hasattr(self,"driver"):
				if self.driver:
					self.driver.quit()
			if hasattr(self,"db"):
				if self.db:
					self.db.close()
		except:
			pass
	def close(self):
		try:
			if hasattr(self,"driver"):
				if self.driver:
					self.driver.quit()
			if hasattr(self,"db"):
				if self.db:
					self.db.close()
		except:
			pass
	def check(self):
		query = 'div[class=\"gt_input\"]'
		res = self.driver.find_elements_by_css_selector(query)
		if not len(res):
			return
		info("CAPTCHA!", layout = self.layout)
		if mode == "test" or mode == "run": self.db.captchaIP(ip)
		sys.exit(0)
		input()
	def getId(self, word):
		noresult = "div[ng-if=\"showNoResult\"]"
		query = 'a[class*=\"query_name\"]'
		footer = 'div[class*=\"search_pager\"]>ul>li'
		total = 'div[class*=\"total\"]'
		self.driver.implicitly_wait(delay)
		ans = []
		pageid = 1
		badass = 0
		pcount = 50
		while True:
			if pageid > pcount:
				info("%4s  over"%(word), layout = self.layout)
				break
			url = 'http://www.tianyancha.com/search/p%d?key=%s&searchType=company'%(pageid,urllib.parse.quote(word))
			self.driver.get(url)
			resList = self.driver.find_elements_by_css_selector(query)
			if len(resList) > 0:
				if pageid == 1:
					pagecount = self.driver.find_elements_by_css_selector(total)
					text = pagecount[0].text
					ret = self.getpage.findall(text)
					if len(ret):
						pcount = int(ret[0])
				hrefList = map(lambda x:x.get_attribute('href'),resList)
				hrefStr = ' '.join(hrefList)
				ret = self.getcid.findall(hrefStr)
				if not len(ret):
					continue
				for pid in ret:
					self.db.addId(pid)
				info("%4s  %02d/%02d  %02d"%(word,pageid,pcount,len(ret)), layout = self.layout)
				pageid += 1
				badass = 0
			else:
				if badass >= 12:
					info("%4s    break"%(word), layout = self.layout)
					break
				else:
					if pageid == 1:
						badass += 12
					else:
						badass += 1
					info("%4s  %02d/%02d  badass"%(word,pageid,pcount), layout = self.layout)
					#info(url)
					#print(self.driver.page_source)
					#exit(0)
				self.check()
		return ans
	def getData(self, tyc_id, checkAlias = True):
		url = 'http://www.tianyancha.com/company/%s' % urllib.parse.quote(str(tyc_id))
		errorpage = "div[class*=errorpage]"
		newname = "span[ng-if=newNameObj]"
		nnhref = "/company/([0-9]*)"
		badass = 0
		while True:
			# info("wait get", layout = self.layout)
			self.driver.get(url)
			# info("get data", layout = self.layout)
			self.driver.implicitly_wait(delay)
			if checkAlias:
				nname = self.driver.find_elements_by_css_selector('span[ng-if=\"newNameObj\"] > a')
				# info("checkAlias", layout = self.layout)
				# self.driver.get_screenshot_as_file('show.png')
				if len(nname) > 0:
					href = nname[0].get_attribute('href')
					regex = re.compile("/company/([0-9]*)")
					ret = regex.findall(href)
					if len(ret):
						info("alias:",ret[0], layout = self.layout)
						self.db.addAlias(tyc_id,ret[0])
						self.db.addId(tyc_id)
						# self.getData(ret[0], False)
			name = self.driver.find_elements_by_css_selector('div[class*=\"company-content\"]')
			# info("check first", layout = self.layout)
			ans = []
			print(self.driver.title)
			if len(name) > 0:
				data = name[0].text.split('\n')
				ans.extend(data)
			else:
				self.check()
				if badass < 2:
					badass += 1
					info("    %s  badass"%tyc_id, layout = self.layout)
					time.sleep(0.5)
					continue
				info("    %s  ret %s"%(tyc_id,retcount), layout = self.layout)
				return None
			name = self.driver.find_elements_by_css_selector('table[class*=\"companyInfo-table\"]')
			# info("check second", layout = self.layout)
			#print("content:",name)
			if len(name) > 0:
				data = name[0].text.split('\n')
				# print(data)
				# ans.append(data[0]+data[2])
				# ans.append(data[1]+data[3])
				# ans.append(data[4]+data[6])
				# ans.append(data[5]+data[7])
				# data = name[1].text.split('\n')
				# print(data)
				ans.extend(data)
			else:
				if badass < 2:
					badass += 1
					info("    %s  badass"%tyc_id, layout = self.layout)
					time.sleep(0.5)
					continue
				# self.check()
				info("    %s  ret %s"%(tyc_id,retcount), layout = self.layout)
				return None
			info("    %s  over"%tyc_id, layout = self.layout)
			# print(ans)
			return ans
	def dataParse(self, data, tyc_id):
		useful = {
			"org_id":"组织机构代码：",
			"reg_id":"工商注册号：",
			"credit_id":"统一信用代码：",
			"legal_person":"法定代表人：",
			"reg_capital":"注册资本：",
			"reg_address":"注册地址：",
			"reg_time":"注册时间：",
			"reg_institution":"登记机关：",
			"enterprise_type":"企业类型：",
			"issue_time":"核准日期：",
			"business_status":"状态：",
			"business_term":"营业期限：",
			"business_type":"行业：",
			"business_scope":"经营范围："
		}
		ret = {}
		#
		ret["name"] = data[0]
		findA = ret["name"].find("--")
		if findA >= 0:
			ret["name"] = ret["name"][findA+len("--"):].strip()
		#
		findB = ret["name"].find("曾用名：")
		if findB >= 0:
			ret["oldname"] = ret["name"][findB+len("曾用名："):].strip()
			ret["name"] = ret["name"][:findB].strip()
			if ret["oldname"] == "": del ret["oldname"]
		#
		findC = ret["name"].find("已更名为：")
		if findC >= 0:
			ret["newname"] = ret["name"][findC+len("已更名为："):].strip()
			ret["name"] = ret["name"][:findC].strip()
			if ret["newname"] == "": del ret["newname"]
		#
		ret["tyc_id"] = tyc_id
		for line in data:
			for key,val in useful.items():
				if line[:len(val)] == val:
					if line[len(val):].strip() != "未公开"and line[len(val):].strip() != "暂无":
						ret[key] = line[len(val):].strip()
		# print(ret)
		return ret
	def dataWork(self, tyc_id):
		global lock,overcount,retcount
		info("  %s"%tyc_id, layout = self.layout)
		ret = self.getData(tyc_id)
		if not ret:
			#time.sleep(1)
			self.db.updateId(tyc_id,0)
			with lock:
				retcount += 1
			return
		with lock:
			overcount += 1
		obj = self.dataParse(ret,tyc_id)
		#info(obj)
		self.db.pushData(obj)
		self.db.updateId(tyc_id,1)
	def idL(self):
		word = self.db.getWord()
		if not word:
			return False
		self.getId(word)
		self.db.updateWord(word,1)
		return True
	def idLoop(self):
		while True:
			self.idL()
	def dataL(self):
		tyc_id = self.db.getId()
		# tyc_id = self.db.getIdSp()
		if not tyc_id:
			return False
		self.dataWork(tyc_id)
		return True
	def dataLoop(self):
		while True:
			self.dataL()
	def spLoop(self, word, pageid = 1):
		pass
	def initWord(self, wordlist):
		for word in wordlist:
			if word:
				self.db.addWord(word)
	def wordLoop(self):
		while True:
			a = input()
			a = a.strip()
			if a:
				self.db.addWord(a)
			else:
				break
	def mainLoop(self):
		global retcount,overcount,lock
		i = 50
		while i:
			while i and self.idL():
				i -= 1
				with lock:
					if retcount >= 2 and overcount == 0:
						sys.exit(0)
			while i and self.dataL():
				i -= 1
				with lock:
					if retcount >= 2 and overcount == 0:
						sys.exit(0)
	def testData(self, tyc_id):
		ret = self.getData(tyc_id)
		if not ret:
			return
		obj = self.dataParse(ret,tyc_id)
		print(obj)
def idWork():
	lo = 0
	global layout,lock
	with lock:
		#print(self.layout)
		lo = layout
		layout += 1
	while True:
		try:
			sp = Spider(lo)
			sp.idLoop()
			sp.dataLoop()
		except Exception as e:
			print(e)
def dataWork():
	lo = 0
	global layout,lock
	with lock:
		#print(self.layout)
		lo = layout
		layout += 1
	while True:
		try:
			sp = Spider(lo)
			sp.dataLoop()
			sp.idLoop()
		except Exception as e:
			print(e)
def mainWork():
	lo = 0
	global layout,lock
	with lock:
		#print(self.layout)
		lo = layout
		layout += 1
		layout %= 8
	while True:
		try:
			sp = Spider(lo)
			sp.mainLoop()
		except Exception as e:
			print(e)
def spWork():
	lo = 0
	while True:
		try:
			sp = Spider(lo)
			sp.mainLoop()
		except Exception as e:
			print(e)
		finally:
			sp.close()

#main
for i in range(2):
	th = threading.Thread(target=mainWork)
	# th.setDaemon(True)
	th.start()

db = DB()
index = 0
flag = False
while True:
	if db.getStatus(ip) == "CAPTCHA":
		break
	if index >= 60 and overcount == 0:
		if mode == "test" and db.getStatus(ip) != "CAPTCHA":  db.badIp(ip)
		if mode == "run" and db.getStatus(ip) != "CAPTCHA":  db.loseIp(ip)
		if db.getStatus(ip) != "CAPTCHA":
			print("time over")
			break
		else:
			break
	if overcount == 0 and retcount >=2:
		if mode == "test":  db.badIp(ip)
		if mode == "run":  db.loseIp(ip)
		break
	if not flag and overcount != 0:
		if mode == "test": db.goodIp(ip)
		flag = True
	time.sleep(6)
	index += 1
db.close()

# threading.Thread(target=endWork).start()
# while True:
# 	try:
# 		sp = Spider(0)
# 		sp.mainLoop()
# 	except Exception as e:
# 		print(e)
# 	finally:
# 		del sp

# 单次测试
# sp = Spider(0)
# print(sp.getData(150041670))