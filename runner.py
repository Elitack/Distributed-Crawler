# coding = utf-8

import sys
import os
import time

import dao

db = dao.SQL()
data = db.getGoodIp()

for ip in data:
	if ip == "": continue
	print(ip)
	command = "start /min cmd /c python spider.py run %s "%ip
	os.system(command)
	time.sleep(0.5)
command = "start /min cmd /c python spider.py local"
os.system(command)
h = set(data)

while True:
	data = db.getGoodIp()
	if data:
		for ip in data:
			if ip == "": continue
			if ip in h: continue
			print(ip)
			command = "start /min cmd /c python spider.py run %s "%ip
			os.system(command)
			time.sleep(0.5)
	h = set(data)
	time.sleep(10)
