import redis


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
        return self.red.get(key)


cache = Cache(host="localhost", port=6379)