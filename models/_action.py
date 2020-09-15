from models import db
from .goods import Goods
from .order import Order, OrderItem
from utils.errors import NotEnough, ParamError


def buy(user, goods_list):
    """
    goods_list = [{"id": 111, "amount": 1}]
    """
    if not isinstance(goods_list, (list, tuple)):
        raise ParamError(
            "goods_list should be type of list, but {} found".format(
                type(goods_list)))
    order = None
    with db.atomic() as transaction:
        try:
            order = Order.create_data(user=user)
            for goods in goods_list:
                goods_id, amount = goods["id"], goods["amount"]
                goods = Goods.check_amount(goods_id=goods_id, amount=amount)
                if not goods:
                    raise NotEnough()
                OrderItem.create_data(order=order.uid,
                                      goods=goods.uid,
                                      price=goods.price,
                                      amount=amount)
                goods.amount -= amount
                goods.save()
        except NotEnough:
            transaction.rollback()
            order = None
        except Exception as e:
            print(e)
            transaction.rollback()
            order = None
    return order