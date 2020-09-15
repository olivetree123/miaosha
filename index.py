import json
from flask import Flask, request
from flask_restful import Resource
from api import api
from flask_script import Manager
from flask_apidoc import ApiDoc
from flask_apidoc.commands import GenerateApiDoc

from models import db
from models.init import create_tables, init_goods
# from utils.response import MESSAGE

app = Flask(__name__)
api.init_app(app)
doc = ApiDoc(app=app)
manager = Manager(app)
manager.add_command("apidoc", GenerateApiDoc())
create_tables()
init_goods()

# @app.before_request
# def _db_connect():
#     if db.is_closed():
#         db.connect()

# @app.teardown_request
# def _db_close(exc):
#     if not db.is_closed():
#         db.close()

# @app.after_request
# def after_request(response):
#     response.headers.add('Access-Control-Allow-Origin', '*')
#     response.headers.add('Access-Control-Allow-Headers',
#                          'Content-Type,Authorization')
#     response.headers.add('Access-Control-Allow-Methods',
#                          'GET,POST,PUT,DELETE,OPTIONS')
#     return response

if __name__ == '__main__':
    # app.run(host="0.0.0.0", debug=True, port=PORT)
    # manager.run(host="0.0.0.0", debug=True, port=PORT)
    manager.run()
