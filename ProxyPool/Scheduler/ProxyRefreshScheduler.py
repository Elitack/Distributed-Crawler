import time
from Manger.ProxyManger import ProxyManger
from Util.HelpFunction import checkProxy

from threading import Thread


class ProxyRefreshScheduler(ProxyManger):
    def __init__(self):
        ProxyManger.__init__(self)

    def validProxy(self):
        self.db.changeName(self.raw_proxy_queue)

        raw_proxy = self.db.pop()
        self.db.changeName(self.useful_proxy_queue)
        exist_proxy = self.db.getList()

        while raw_proxy:
            if checkProxy(raw_proxy) and (raw_proxy not in exist_proxy):
                self.db.changeName(self.useful_proxy_queue)
                self.db.put(raw_proxy)
                print("%s is useful" % raw_proxy)
            else:
                print("%s is useless" % raw_proxy)

            self.db.changeName(self.raw_proxy_queue)
            raw_proxy = self.db.pop()


def refreshPool():
    pp = ProxyRefreshScheduler()
    pp.validProxy()


def main(process_num=8):
    p = ProxyRefreshScheduler()
    p.refresh()

    pl = []
    for num in range(process_num):
        proc = Thread(target=refreshPool(), args=())
        pl.append(proc)

    for num in range(process_num):
        pl[num].start()

    for num in range(process_num):
        pl[num].join()

    print(p.db.getNumber())

if __name__ == "__main__":
    main()