from peewee import CharField, BooleanField, SmallIntegerField, DateField, ForeignKeyField, UUIDField, DecimalField, IntegerField

from models import BaseModel, db


class Order(BaseModel):
    user = UUIDField(index=True, verbose_name="用户")


class OrderItem(BaseModel):
    order = UUIDField(index=True, verbose_name="订单id")
    goods = UUIDField(index=True, verbose_name="商品id")
    price = DecimalField(verbose_name="成交价格")
    amount = IntegerField(verbose_name="购买数量")
    