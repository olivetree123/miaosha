from models import db
from .user import User
from .goods import Goods
from .order import Order, OrderItem
from cache import cache
from utils.errors import GoodsNotEnough, MoneyNotEnough, ParamError, DataNotFound
"""
购买的过程可以有3种实现方式：
1. 使用 MySQL 的事务
2. 使用 Redis 缓存，可以提高性能
3. 使用 MongoDB，既可以提高性能，又能保证数据不丢失
4. 使用 Redis 缓存，并保证宕机时尽量多的恢复数据

已知的问题：
问题1：user.uid 是不是每次使用都会去查询数据库？
问题2：在事务过程中，其他事务能否修改它所用到的数据？
问题3：完全使用缓存的数据，如何保证极端情况下数据不丢失？
"""


def buy(user_uid, goods_list):
    """
    goods_list = [{"id": 111, "amount": 1}]
    还应该判断货币是否足够，并扣除货币
    """
    if not isinstance(goods_list, (list, tuple)):
        raise ParamError(
            "goods_list should be type of list, but {} found".format(
                type(goods_list)))
    order = None
    with db.atomic() as transaction:
        try:
            user = User.get_with_uid(user_uid)
            if not user:
                raise DataNotFound(
                    "user not found for uid={}".format(user_uid))
            order = Order.create_data(user=user_uid)
            for goods in goods_list:
                goods_id, amount = goods["id"], goods["amount"]
                goods = Goods.check_amount(goods_id=goods_id, amount=amount)
                if not goods:
                    raise GoodsNotEnough()
                if user.money < goods.price:
                    raise MoneyNotEnough()
                OrderItem.create_data(order=order.uid,
                                      goods=goods.uid,
                                      price=goods.price,
                                      amount=amount)
                user.money -= goods.price
                goods.amount -= amount
                user.save()
                goods.save()
        except GoodsNotEnough:
            transaction.rollback()
            order = None
        except MoneyNotEnough:
            transaction.rollback()
            order = None
        except Exception as e:
            print(e)
            transaction.rollback()
            order = None
    return order


def buy_from_cache(user_id, goods_list):
    """
    库存放在缓存中，但是要怎么生成订单并扣除货币呢？
    用户信息不可以在缓存中操作，因为用户可以买其他商品，而其他商品的购买是常规的 mysql 操作。
    """
    if not isinstance(goods_list, (list, tuple)):
        raise ParamError(
            "goods_list should be type of list, but {} found".format(
                type(goods_list)))


def buy_from_mongo(user_id, goods_list):
    """使用 MongoDB"""
    pass