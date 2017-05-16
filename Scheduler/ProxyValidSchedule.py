


from Util.HelpFunction import checkProxy
from Manager.ProxyManager import ProxyManager


class ProxyValidSchedule(ProxyManager):
    def __init__(self):
        ProxyManager.__init__(self)

    def __validProxy(self):
        """
        验证代理
        :return:
        """
        while True:
            self.db.changeTable(self.useful_proxy_queue)
            for each_proxy in self.db.getAll():
                if isinstance(each_proxy, bytes):
                    each_proxy = each_proxy.decode('utf-8')

                if checkProxy(each_proxy):
                    self.log.debug('validProxy_b: {} validation pass'.format(each_proxy))
                else:
                    self.db.delete(each_proxy)
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