#coding:utf-8
from flask import request
from flask_httpauth import HTTPTokenAuth

from config import TOKEN_SCHEME
from cache import cache

token_auth = HTTPTokenAuth(scheme=TOKEN_SCHEME)


@token_auth.verify_token
def verify_token(token):
    if not token:
        return False
    user_id = cache.get_token(token)
    if not user_id:
        return False
    setattr(request, "user", user_id)
    return True
