import requests
from time import sleep
from lxml import etree

from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def getHTMLTree(url):
    header = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
    }
    if "www.kuaidaili.com" in url:
        sleep(1)

    r = requests.get(url=url, headers=header, timeout=30)
    html = r.content
    HTMLTree = etree.HTML(html)
    return HTMLTree


def checkProxy(proxy):
    if "https" in proxy:
        proxies = {
            "https": proxy,
        }
    else :
        proxies = {
            "http": proxy,
        }

    try:
        r = requests.get('http://www.tianyancha.com/', proxies=proxies, timeout=5, verify=False)
        if r.status_code == 200:
            return True

    except Exception as e:
        print(e)
        return False

if __name__ == "__main__":
    print(checkProxy("https://208.92.94.142:1080"))
