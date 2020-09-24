import redis
from config import REDIS_HOST, REDIS_PORT


class Cache(object):
    def __init__(self, host, port):
        self.red = redis.Redis(host=host, port=port)

    def set(self, key, value):
        self.red.set(key, value)

    def get(self, key):
        return self.red.get(key)

    def set_token(self, token, user_id):
        key = "MIAOSHA:TOKEN:{TOKEN}".format(TOKEN=token)
        self.red.set(key, user_id)

    def get_token(self, token):
        key = "MIAOSHA:TOKEN:{TOKEN}".format(TOKEN=token)
        return str(self.red.get(key), encoding="utf8")

    def run_script(self, script):
        return self.red.register_script(script)


cache = Cache(host=REDIS_HOST, port=REDIS_PORT)