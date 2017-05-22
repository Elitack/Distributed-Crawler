
import sys

sys.path.append('../')

from Util.HelpFunction import checkProxy
from Manager.ProxyManager import ProxyManager


class ProxyValidSchedule(ProxyManager):
    def __init__(self):
        ProxyManager.__init__(self)

    def __validProxy(self):

        while True:
            self.db.changeName(self.raw_proxy_queue)
            for each_proxy in self.db.getList():
                if isinstance(each_proxy, bytes):
                    each_proxy = each_proxy.decode('utf-8')
                if checkProxy(each_proxy):
                    self.db.changeName(self.useful_proxy_queue)
                    self.db.put(each_proxy)
                    print (each_proxy)
                    self.db.changeName(self.raw_proxy_queue)
                else:
                    self.db.delete(each_proxy)

    def main(self):
        self.__validProxy()


def run():
    p = ProxyValidSchedule()
    p.main()


if __name__ == '__main__':
    p = ProxyValidSchedule()
    p.main()