from models import db
from .user import User
from .goods import Goods
from .mongo import Goods2, Order2, OrderItem2
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


def buy_from_redis(user_uid, goods_list):
    """
    使用Redis，使用lua脚本保证操作的原子性
    goods_list = [{"id": "111", "amount": 2}]
    goods_list_str = "111:2;222:3"
    """
    lua_script = """
        local function split(inputstr, sep)
            if sep == nil then
                sep = "%s"
            end
            local t = {{}}
            for str in string.gmatch(inputstr, "([^"..sep.."]+)") do
                table.insert(t, str)
            end
            return t
        end

        local function get_goods_list(goods_list_str)
            local result = {{}}
            local data = split(goods_list_str, ";")
            for i, goods in ipairs(data) do
                local d = split(goods, ":")
                result[d[1]] = d[2]
            end
            return result
        end

        local function log(message)
            redis.log(redis.LOG_NOTICE, message)
        end

        local user_id = "{USER_ID}"
        local goods_list_str = "{GOODS_LIST_STR}"
        local goods_list = get_goods_list(goods_list_str)
        local order_key = "MIAOSHA:ORDER:"..user_id
        for goods_id, amount in pairs(goods_list) do
            local goods_key = "MIAOSHA:GOODS:"..goods_id
            local amt = redis.call("get", goods_key)
            if amt < amount then
                return 0
            end
        end
        local items = ""
        for goods_id, amount in pairs(goods_list) do
            local item = goods_id..":"..amount..";"
            local goods_key = "MIAOSHA:GOODS:"..goods_id
            redis.call("decrby", goods_key, amount)
            items = items..item
        end
        redis.call("lpush", order_key, items)
        log("success to crete order, order_key = "..order_key)
        return 1
    """
    goods_list_str = []
    for goods in goods_list:
        goods_list_str.append(goods["id"] + ":" + str(goods["amount"]))
    goods_list_str = ";".join(goods_list_str)
    script = lua_script.format(USER_ID=user_uid, GOODS_LIST_STR=goods_list_str)
    cmd = cache.run_script(script)
    res = cmd()
    return None


def buy_from_mongo(user_uid, goods_list):
    """
    使用 MongoDB
    好像不支持事务 ？
    """
    print("user_uid = ", user_uid)
    items = []
    for goods in goods_list:
        goods_id, amount = goods["id"], goods["amount"]
        goods = Goods2.check_amount(goods_id, amount)
        if not goods:
            raise GoodsNotEnough()
        goods.amount -= amount
        goods.save()
        item = OrderItem2(goods=goods, price=goods.price, amount=amount)
        items.append(item)
    order = Order2(user=user_uid, items=items)
    order.save()
    return order