import redis
import json


class RedisClient(object):
    def __init__(self, name, host, port):
        self.name = name
        self.conn = redis.Redis(host=host, port=port, db=0)

    def get(self):
        return self.conn.srandmember(name=self.name)

    def put(self, value):
        value = json.dumps(value) if isinstance(value, (dict, list)) else value
        return self.conn.sadd(self.name, value)

    def pop(self):
        if self.conn.scard(self.name) == 0:
            return None
        else:
            self.conn.spop(self.name)

    def delete(self, value):
        self.conn.srem(self.name, value)

    def getList(self):
        return self.conn.smembers(self.name)

    def getNumber(self):
        return self.conn.scard(self.name)

    def changeName(self, name):
        self.name = name

    def deleteAll(self, name):
        while self.conn.scard(name) != 0:
            self.conn.spop(name)

if __name__ == "__main__":
    redis_conn = RedisClient('useful_proxy', 'localhost', 6379)
    redis_conn.put("0.0.0.0:0000")


    print(redis_conn.getList())