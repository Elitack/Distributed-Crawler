
import sys

sys.path.append('../')

from Util.HelpFunction import checkProxy
from Manager.ProxyManager import ProxyManager


class ProxyValidSchedule(ProxyManager):
    def __init__(self):
        ProxyManager.__init__(self)

    def __validProxy(self):

        while True:
            self.db.changeName(self.useful_proxy_queue)
            for each_proxy in self.db.getList():
                if isinstance(each_proxy, bytes):
                    each_proxy = each_proxy

                if checkProxy(each_proxy):
                    self.log.debug('validProxy_b: {} validation pass'.format(each_proxy))
                    print (each_proxy + "pass")
                else:
                    self.db.delete(each_proxy)
                    print (each_proxy)
                    self.log.info('validProxy_b: {} validation fail'.format(each_proxy))
        self.log.info('validProxy_a running normal')

    def main(self):
        self.__validProxy()


def run():
    p = ProxyValidSchedule()
    p.main()


if __name__ == '__main__':
    p = ProxyValidSchedule()
    p.main()