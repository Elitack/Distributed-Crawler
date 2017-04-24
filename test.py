import requests
import threading
import time
if not []:
	print("1")

# session = requests.session()
# data = {"status":"123"}
# res = session.post("http://localhost/api/ip/111.111.11.11",data=data)
# print(res.text)

# lock = threading.Lock()

# def mainWork():
# 	while True:
# 		with lock:
# 			print("a")
# 			print(lock)
# 			time.sleep(1)

# def endWork():
# 	while True:
# 		with lock:
# 			print("exit")
# 			print(lock)
# 			exit(0)

# threading.Thread(target=mainWork).start()
# threading.Thread(target=endWork).start()

# headers = {
# "Accept-Encoding":"gzip, deflate, sdch",
# "Accept-Language":"zh-CN,zh;q=0.8",
# "Cache-Control":"no-cache",
# "Connection":"keep-alive",
# "Host":"www.tianyancha.com",
# "Pragma":"no-cache",
# "Referer":"http://www.tianyancha.com/company/2323344796",
# "Tyc-From":"normal",
# "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36",
# "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
# "Accept":"application/json, text/plain, */*",
# "Tyc-From": "normal",
# "Tyc-Click": None,
# "Tyc-Ab": None,
# "CheckError": "check",
# "Cookie":"token=44573a2ba5934135ab13dade04de54ea; _utm=cb3740ab9bcf48088ca84da645e6f639"

# }
# session = requests.session()
# res = session.get("http://www.tianyancha.com")
# print(res.status_code)
# res = session.get("http://www.tianyancha.com/tongji/2327295991.json?random=1480935682845",headers = headers)
# print(res.text)
# res = session.get("http://www.tianyancha.com/IcpList/2327295991.json",headers = headers)
# print(res.text)
# res = session.get("http://www.tianyancha.com/company/2327295991.json",headers = headers)
# print(res.text)
# res = session.get("http://www.tianyancha.com/company/2327295991.json",headers = headers)
# print(res.text)
