import random
from models import db
from models.user import User
from models.goods import Goods
from models.order import Order, OrderItem
from models.mongo import Goods2

MODEL_LIST = [User, Goods, Order, OrderItem]


def create_tables():
    db.create_tables(MODEL_LIST)


def init_goods():
    goods = Goods.get_or_none(name="商品1000000")
    if not goods:
        i = 1000000
        while i < 1000010:
            name = "商品{}".format(i)
            price = random.uniform(10, 100)
            amount = random.randint(0, 10)
            Goods.create_data(name=name, price=price, amount=amount)
            i += 1
    count = Goods2.objects.count()
    if count == 0:
        i = 1000000
        while i < 1000010:
            name = "商品{}".format(i)
            price = random.uniform(10, 100)
            amount = random.randint(0, 10)
            g = Goods2(name=name, price=price, amount=amount)
            g.save()
            i += 1
