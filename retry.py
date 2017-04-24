import requests
import threading
import time
import dao
import queue

db = dao.SQL()
data = db.getBadIp()
works = queue.Queue()
print(len(data))

for ip in data:
	works.put(ip)

def test():
	global db,works
	proxies = {
		"http": "http://139.129.128.134:3128"
	}
	session = requests.session()
	while works.qsize():
		ip = works.get()
		proxies["http"] = ip
		try:
			res = session.get("http://www.tianyancha.com",proxies = proxies,timeout = 10)
			print(ip,res.status_code)
			if res.status_code == 200:
				db.testIp(ip)
		except Exception as e:
			print(ip,e)
			pass
		# input("next")
		works.task_done()

for i in range(10):
	th = threading.Thread(target=test)
	# th.setDaemon(True)
	th.start()