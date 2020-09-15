import random
from models import db
from models.user import User
from models.goods import Goods
from models.order import Order, OrderItem

MODEL_LIST = [User, Goods, Order, OrderItem]


def create_tables():
    db.create_tables(MODEL_LIST)


def init_goods():
    goods = Goods.get_or_none(name="商品1000000")
    if goods:
        print("已经有商品了，不需要再初始化商品")
        return
    print("开始初始化商品")
    i = 1000000
    while i < 1000010:
        name = "商品{}".format(i)
        price = random.uniform(10, 100)
        amount = random.randint(0, 10)
        Goods.create_data(name=name, price=price, amount=amount)
        i += 1