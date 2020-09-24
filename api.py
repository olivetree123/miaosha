#coding:utf-8

from flask_restful import Api

from handlers.signup import SignUpEndpoint
from handlers.login import LoginEndpoint
from handlers.deal import OrderEndpoint, Order2Endpoint, Order3Endpoint

api = Api()

api.add_resource(SignUpEndpoint, "/api/signup")
api.add_resource(LoginEndpoint, "/api/login")
api.add_resource(OrderEndpoint, "/api/buy")
api.add_resource(Order2Endpoint, "/api/buy2")
api.add_resource(Order3Endpoint, "/api/buy3")
