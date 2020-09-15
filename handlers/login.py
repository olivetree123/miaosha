import uuid
from flask import request
from flask_apidoc import ApiDoc
from flask_restful import Resource, marshal_with

from auth import token_auth
from models.user import User
from cache import cache
from base import resource_fields, APIResponse
from utils.response import BAD_REQUEST, ACCOUNT_DUPLICATE, ACCOUNT_NOT_FOUND, LOGIN_FAILED


class LoginEndpoint(Resource):
    decorators = [marshal_with(resource_fields)]

    def post(self):
        """
        @api {POST} /api/login 登陆
        @apiName LogIn
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
        if not status:
            return APIResponse(code=ACCOUNT_NOT_FOUND)
        user = User.cipher_validate(account=params["account"],
                                    cipher=params["cipher"])
        if not user:
            return APIResponse(code=LOGIN_FAILED)
        user = user.json()
        user.pop("cipher", None)
        token = uuid.uuid4().hex
        user["token"] = token
        cache.set_token(token, user["uid"])
        return APIResponse(data=user)
