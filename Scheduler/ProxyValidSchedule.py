from Manger.ProxyManger import ProxyManger
from Util.HelpFunction import checkProxy


class ProxyValidSchedule(ProxyManger):
    def __init__(self):
        ProxyManger.__init__(self)

    def refreshProxy(self):
        self.db.changeName(self.useful_proxy_queue)
        for proxy in self.db.getList():
            if isinstance(proxy, bytes):
                proxy = proxy.decode('utf-8')

            if checkProxy(proxy):
                print("%s is valid" % proxy)
            else:
                self.db.delete(proxy)
                print("%s is deleted" % proxy)

    def main(self):
        self.refresh()


def run():
    p = ProxyValidSchedule()
    p.main()

if __name__ == '__main__':
    run()