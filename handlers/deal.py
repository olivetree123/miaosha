from flask import request
from flask_apidoc import ApiDoc
from flask_restful import Resource, marshal_with

from auth import token_auth
from models.goods import Goods
from models.order import Order, OrderItem
from models._action import buy, buy_from_mongo, buy_from_redis
from base import resource_fields, APIResponse
from utils.response import BAD_REQUEST, INVENTORY_NOT_ENOUGH, ORDER_FAILED


class OrderEndpoint(Resource):
    decorators = [marshal_with(resource_fields), token_auth.login_required]

    def get(self, uid):
        """
        @api {GET} /api/order/<uid> 获取用户信息
        @apiName GetOrder
        @apiGroup Order

        @apiExample 返回值
        {
            "code": 0,
            "message": null,
            "data": null
        }
        """
        r = Order.get_with_uid(uid)
        return APIResponse(data=r)

    def post(self):
        """
        @api {POST} /api/order 创建订单
        @apiName CreateOrder
        @apiGroup Order

        @apiExample 参数
        {
            "goods": [{"id": "111", "amount": 5}]
        }

        @apiExample 返回值
        {
            "code": 0,
            "message": null,
            "data": null
        }
        """
        params = request.get_json()
        if not params:
            return APIResponse(code=BAD_REQUEST)
        order = buy(request.user, params["goods"])
        if not order:
            return APIResponse(code=ORDER_FAILED)
        return APIResponse(data=order)


class Order2Endpoint(Resource):
    decorators = [marshal_with(resource_fields), token_auth.login_required]

    def post(self):
        params = request.get_json()
        if not params:
            return APIResponse(code=BAD_REQUEST)
        order = buy_from_mongo(request.user, params["goods"])
        if not order:
            return APIResponse(code=ORDER_FAILED)
        return APIResponse(data=order.to_json())


class Order3Endpoint(Resource):
    decorators = [marshal_with(resource_fields), token_auth.login_required]

    def post(self):
        params = request.get_json()
        if not params:
            return APIResponse(code=BAD_REQUEST)
        order = buy_from_redis(request.user, params["goods"])
        if not order:
            return APIResponse(code=ORDER_FAILED)
        return APIResponse(data=order)