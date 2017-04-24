#!/usr/bin/python
# -*- coding: UTF-8 -*-
import pymysql
import random
import warnings
import time
#warnings.filterwarnings("ignore")

from uuid import uuid1 as uuid
def toStr(func):
	def _func(*args, **kwargs):
		ret = func(*args, **kwargs)
		return str(ret)
	return _func
uuid = toStr(uuid)
def getCon():
	return pymysql.connect(host='',user='',passwd='',db='enterprise',port=3306,charset='utf8', cursorclass = pymysql.cursors.DictCursor)
def addItem(func):
	def work(self, table, key, args, **unuse):
		value = ["%s"]*(len(key)-2)
		query = "INSERT INTO %s (%s) VALUES (%s,CURRENT_TIMESTAMP,0);"%(table,','.join(key),','.join(value))
		try:
			con = getCon()
			cur = con.cursor()
			cur.execute(query, args)
			cur.close()
			con.commit()
			return True
		except Exception as e:
			con.rollback()
			return False
		except pymysql.Warning as e:
			pass
		finally:
			con.close()
	def _func(self, arg):
		if not arg:
			return False
		ret = func(self, arg)
		return work(**ret)
	return _func
def getItem(func):
	def work(self, table, gap, limit, column, **unuse):
		query = "SELECT * FROM (select * from %s WHERE DATE_SUB(NOW(), INTERVAL %d DAY) > `timestamp`) as t1 where `id` >= (select max(id) from %s)*rand() LIMIT %d;"%(table,gap,table,limit)
		# print(query)
		try:
			con = getCon()
			cur = con.cursor()
			cur.execute(query)
			data = cur.fetchall()
			cur.close()
			if not len(data):
				query = "SELECT * FROM (select * from %s WHERE count=0) as t1 where `id` >= (select max(id) from %s)*rand() LIMIT %d;"%(table,table,limit)
				try:
					cur = con.cursor()
					cur.execute(query)
					data = cur.fetchall()
					cur.close()
					if len(data) == 0:
						return None
					item = random.choice(data)[column]
					return item
				except Exception as e:
					print(e)
					return None
			item = random.choice(data)[column]
			return item
		except Exception as e:
			print(e)
			return None
		except pymysql.Warning as e:
			pass
		finally:
			con.close()
	def _func(self):
		ret = func(self)
		return work(**ret)
	return _func
def updateItem(func):
	def work(self, table, key, args, count, **unuse):
		value = ["%s"]*(len(key)-2)
		query = "INSERT INTO %s (%s) VALUES(%s,CURRENT_TIMESTAMP,0) ON DUPLICATE KEY UPDATE count = count+%d;"%(table,','.join(key),','.join(value),count)
		#print(query)
		try:
			con = getCon()
			cur = con.cursor()
			cur.execute(query, args)
			cur.close()
			con.commit()
			return True
		except Exception as e:
			print(e)
			con.rollback()
			return False
		finally:
			con.close()
	def _func(self, arg, count):
		if not arg:
			return False
		ret = func(self, arg)
		ret["count"] = count
		return work(**ret)
	return _func

class SQL:
#{
	def __init__(self):
		# con = pymysql.connect(host='dsql.c.liminfi.com',user='root',passwd='aaa111!!!',db='enterprise',port=3306,charset='utf8', cursorclass = pymysql.cursors.DictCursor)
		self.table = None
	def __del__(self):
		try:
			if hasattr(self,"con"):
				if con:
					con.close()
		except:
			pass
	def close(self):
		try:
			if hasattr(self,"con"):
				if con:
					con.close()
		except:
			pass
	def setTable(self, table):
		self.table = table
		return table
	def getAll(self, table = None):
		if not table:
			table = self.table
		if not table:
			return None
		query = "SELECT * FROM %s;"%(table)
		try:
			con = getCon()
			cur = con.cursor()
			cur.execute(query)
			data = cur.fetchall()
			cur.close()
			con.commit()
			return data
		except Exception as e:
			print(e)
			return None
		finally:
			con.close()
	def size(self, table = None):
		if not table:
			table = self.table
		if not table:
			return None
		query = "SELECT COUNT(*) as count FROM %s;"%(table)
		try:
			con = getCon()
			cur = con.cursor()
			cur.execute(query)
			data = cur.fetchall()
			item = data[0]['count']
			cur.close()
			con.commit()
			return item
		except Exception as e:
			print(e)
			return None
		finally:
			con.close()
	def getRecent(self, time = 0, ttype = "DAY", table = None):
		if not table:
			table = self.table
		if not table:
			return None
		query = "SELECT COUNT(*) as count FROM %s WHERE DATE_SUB(NOW(), INTERVAL %d %s) <= `timestamp`;"%(table,time,ttype)
		try:
			con = getCon()
			cur = con.cursor()
			cur.execute(query)
			data = cur.fetchall()
			item = data[0]['count']
			# print(data)
			cur.close()
			con.commit()
			return item
		except Exception as e:
			print(e)
			return None
		finally:
			con.close()
	@addItem
	def addWord(self, word):
		table = "wordtmp"
		key = ["id","word","timestamp","count"]
		args = [None, word]
		return locals()
	@getItem
	def getWord(self):
		table = "wordtmp"
		gap = 30
		limit = 10
		column = 'word'
		return locals()
	@updateItem
	def updateWord(self, word):
		table = "wordtmp"
		key = ["id","word","timestamp","count"]
		value = ["%s"]*len(key)
		args = [None, word]
		return locals()
	@addItem
	def addId(self, tyc_id):
		table = "tyctmp"
		key = ["id","tyc_id","timestamp","count"]
		args = [None, tyc_id]
		return locals()
	@getItem
	def getId(self):
		table = "tyctmp"
		gap = 90
		limit = 10
		column = 'tyc_id'
		return locals()
	@updateItem
	def updateId(self, tyc_id):
		table = "tyctmp"
		key = ["id","tyc_id","timestamp","count"]
		args = [None, tyc_id]
		return locals()
	def pushData(self,data):
		if not data or "name" not in data:
			return False
		table = "directory"
		key = ['id', 'name', 'oldname', 'newname', 'reg_id', 'org_id', 'tax_id', 'credit_id', 'tyc_id', 'saic_id', 'saic_area','legal_person','reg_capital','reg_address','reg_time','reg_institution','enterprise_type','issue_time','business_status','business_term','business_type',"business_scope"]
		value = ["%s"]*len(key)
		args = [data.get(x) for x in key]
		query = "REPLACE INTO %s (%s) VALUES(%s);"%(table,','.join(key),','.join(value))
		#print(query)
		try:
			con = getCon()
			cur = con.cursor()
			cur.execute(query, args)
			cur.close()
			con.commit()
			return True
		except Exception as e:
			print(e)
			con.rollback()
			return False
		finally:
			con.close()
	#@addItem
	def addAlias(self, oid, nid):
		table = "alias"
		key = ["id","oid","nid"]
		args = [None, oid, nid]
		value = ["%s"]*(len(key))
		query = "INSERT INTO %s (%s) VALUES (%s);"%(table,','.join(key),','.join(value))
		try:
			con = getCon()
			cur = con.cursor()
			cur.execute(query, args)
			cur.close()
			con.commit()
			return True
		except Exception as e:
			con.rollback()
			return False
		except pymysql.Warning as e:
			pass
		finally:
			con.close()
		# return locals()
	def check(self):
		query="UPDATE `tyctmp` SET date=0000-00-00 WHERE date!=0000-00-00 AND `tyc_id` NOT IN (select tyc_id FROM directory UNION (SELECT oid FROM alias))"
		try:
			con = getCon()
			cur = con.cursor()
			ret = cur.execute(query)
			cur.close()
			con.commit()
			return ret
		except Exception as e:
			print(e)
			con.rollback()
			return 0
		finally:
			con.close()
	def getIdSp(self):
		query = "SELECT tyc_id FROM `directory` WHERE `newname` = \"\" OR `oldname` = \"\" LIMIT 1000 "
		# print(query)
		try:
			con = getCon()
			cur = con.cursor()
			cur.execute(query)
			data = cur.fetchall()
			cur.close()
			if not len(data):
				return None
			item = random.choice(data)['tyc_id']
			return item
		except Exception as e:
			print(e)
			return None
		finally:
			con.close()
	def getIp(self, status = "GOOD"):
		column = "ip"
		table = "ippool"
		query = "SELECT %s as ip FROM %s WHERE `status` = \"%s\" LIMIT 10000"%(column, table, status)
		# print(query)
		try:
			con = getCon()
			cur = con.cursor()
			cur.execute(query)
			data = cur.fetchall()
			cur.close()
			con.commit()
			if not len(data):
				return []
			return list(map(lambda x: x['ip'], data))
		except Exception as e:
			print(e)
			return None
		finally:
			con.close()
	def updateIp(self, ip, status):
		table = "ippool"
		key = ["id","ip","status","timestamp"]
		value = ["%s"]*(len(key)-1)
		args = [None, ip, status]
		query = "INSERT INTO %s (%s) VALUES(%s,CURRENT_TIMESTAMP) ON DUPLICATE KEY UPDATE status = \"%s\";"%(table,','.join(key),','.join(value), status)
		# print(query)
		try:
			con = getCon()
			cur = con.cursor()
			cur.execute(query,args)
			cur.close()
			con.commit()
			return True
		except Exception as e:
			print(e)
			con.rollback()
			return False
		finally:
			con.close()
	def addIp(self, ip):
		table = "ippool"
		key = ["id","ip","status","timestamp"]
		value = ["%s"]*(len(key)-1)
		args = [None, ip,"TEST"]
		query = "INSERT INTO %s (%s) VALUES (%s,CURRENT_TIMESTAMP);"%(table,','.join(key),','.join(value))
		# print(query)
		try:
			con = getCon()
			cur = con.cursor()
			cur.execute(query,args)
			cur.close()
			con.commit()
			return True
		except Exception as e:
			# print(e)
			con.rollback()
			return None
		finally:
			con.close()
	def getStatus(self, ip):
		column = "status"
		table = "ippool"
		query = "SELECT %s as status FROM %s WHERE `ip` = \"%s\" LIMIT 1"%(column, table, ip)
		# print(query)
		try:
			con = getCon()
			cur = con.cursor()
			cur.execute(query)
			data = cur.fetchall()
			cur.close()
			con.commit()
			if not len(data):
				return None
			return data[0]["status"]
		except Exception as e:
			print(e)
			return None
		finally:
			con.close()
#
	def giveupLose(self):
		table = "ippool"
		from_status = "MISTAKE"
		to_status = "BAD"
		query = "UPDATE %s SET status = \"%s\" WHERE status = \"%s\";"%(table, to_status, from_status)
		# print(query)
		try:
			con = getCon()
			cur = con.cursor()
			cur.execute(query)
			cur.close()
			con.commit()
			return True
		except Exception as e:
			print(e)
			con.rollback()
			return False
		finally:
			con.close()
#get Ip
	def getGoodIp(self):
		return self.getIp("GOOD")
	def getBadIp(self):
		return self.getIp("BAD")
	def getTestIp(self):
		return self.getIp("TEST")
	def getLoseIp(self):
		return self.getIp("MISTAKE")
	def getCaptchaIP(self):
		return self.getIp("CAPTCHA")
#set Ip
	def goodIp(self, ip):
		self.updateIp(ip,"GOOD")
	def badIp(self, ip):
		self.updateIp(ip,"BAD")
	def testIp(self, ip):
		self.updateIp(ip,"TEST")
	def loseIp(self, ip):
		self.updateIp(ip,"MISTAKE")
	def captchaIP(self, ip):
		self.updateIp(ip,"CAPTCHA")
#}
def main():
	db = SQL()
	#print(db.getall())
	# print("word")
	# db.setTable("wordtmp")
	# print(db.size())
	# print(db.getRecent(1,"YEAR"))
	# print("tyctmp")
	# db.setTable('tyctmp')
	# print(db.size())
	# print(db.getRecent(1,"SECOND"))
	# print(db.getRecent(1,"MINUTE"))
	# print(db.getRecent(1,"HOUR"))
	# print(db.getRecent(1,"DAY"))
	# # print(db.getRecent(1,"MONTH"))
	# print("directory")
	# db.setTable("directory")
	# print(db.size())
	# # while True:
	# # 	print(db.getRecent(1,"SECOND"))
	# # 	time.sleep(1)
	# print(db.getId())
	# print(db.getWord())
	# print(db.getIdSp())
	print(db.getIp())
	print(db.getTestIp())
	# while True:
	# 	print(db.getTestIp())
	# 	time.sleep(5)
	# print(db.getStatus("220.194.213.242:8080"))
if __name__ == '__main__':
	main()
