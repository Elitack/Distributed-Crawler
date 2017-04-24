# coding = utf-8

import sys
import os
import time

import dao

db = dao.SQL()
data = db.getLoseIp()

for index,ip in enumerate(data):
	if index and index % 10 == 0: time.sleep(10)
	if index and index % 50 == 0: time.sleep(10)
	if ip == "": continue
	print(ip)
	db.badIp(ip)
	command = "start /min cmd /c python spider.py test %s"%ip
	os.system(command)
	h = set(data)
	time.sleep(5)

while True:
	data = db.getTestIp()
	if data:
		for index,ip in enumerate(data):
			if ip == "": continue
			# if ip in h: continue
			print(ip)
			db.badIp(ip)
			command = "start /min cmd /c python spider.py test %s"%ip
			os.system(command)
			h.add(ip)
			time.sleep(10)
	h = set(data)
	time.sleep(10)