from peewee import CharField, DecimalField, IntegerField

from models import BaseModel, db


class Goods(BaseModel):
    name = CharField(null=False, verbose_name="名称")
    price = DecimalField(default=0, verbose_name="价格")
    amount = IntegerField(default=0, verbose_name="库存")

    @classmethod
    def check_amount(cls, goods_id, amount):
        r = cls.get_or_none(uid=goods_id)
        if r and r.amount > 0 and r.amount >= amount:
            return r
        return False
