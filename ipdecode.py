# coding = utf-8

import sys
import os
import codecs
open = codecs.open
import json
import re
import dao

db = dao.SQL()
while True:
	data = input("input data:")
	if data.strip() == "":
		break
	try:
		rawdata = json.loads(data)
		rawip = []
		for ip in rawdata:
			newip = str(ip['ip'])+":"+str(ip['port'])
			rawip.append(newip)
	except:
		regex = re.compile("((?:[0-9]{1,3}\.){3}[0-9]{1,3})[\t \",\:]*([0-9]*)")
		rawip = regex.findall(data)
		rawip = list(map(lambda x: x[0]+":"+x[1],rawip))
	for newip in rawip:
		if db.addIp(newip):
			print(newip)
	print()