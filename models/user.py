import hashlib
from peewee import CharField

from models import BaseModel, db


class User(BaseModel):
    account = CharField(unique=True, verbose_name="账号")
    cipher = CharField(verbose_name="密码")

    @classmethod
    def is_exists(cls, account):
        r = cls.get_or_none(account=account)
        if not r:
            return False
        return True

    @classmethod
    def cipher_encypt(cls, cipher):
        h = hashlib.md5(cipher.encode("utf8"))
        return h.hexdigest()

    @classmethod
    def cipher_validate(cls, account, cipher):
        h = hashlib.md5(cipher.encode("utf8"))
        value = h.hexdigest()
        return cls.get_or_none(account=account, cipher=value)
