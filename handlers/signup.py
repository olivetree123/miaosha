from flask import request
from flask_apidoc import ApiDoc
from flask_restful import Resource, marshal_with

from auth import token_auth
from models.user import User
from base import resource_fields, APIResponse
from utils.response import BAD_REQUEST, ACCOUNT_DUPLICATE


class SignUpEndpoint(Resource):
    decorators = [marshal_with(resource_fields)]
    
    def post(self):
        """
        @api {POST} /api/signup 注册账号
        @apiName SignUp
        @apiGroup User

        @apiExample 参数
        {
            "account":"olivetree",
            "cipher": "123456"
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
        status = User.is_exists(params["account"])
        if status:
            return APIResponse(code=ACCOUNT_DUPLICATE)
        cipher = User.cipher_encypt(params["cipher"])
        user = User.create_data(account=params["account"], cipher=cipher)
        return APIResponse(data=user)
