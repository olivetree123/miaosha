import hashlib
from peewee import CharField, DecimalField

from models import BaseModel, db


class User(BaseModel):
    account = CharField(unique=True, verbose_name="账号")
    cipher = CharField(verbose_name="密码")
    money = DecimalField(default=0, verbose_name="货币数量")

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

    @classmethod
    def check_money(cls, user_uid, need):
        user = cls.get_with_uid(uid=user_uid)
        if not user:
            return False
        if user.money < need:
            return False
        return True
