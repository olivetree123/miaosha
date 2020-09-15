from flask_restful import fields
from utils.response import MESSAGE
from utils.functions import field_to_json

resource_fields = {
    "code" : fields.Integer,
    "message" : fields.String,
    "data" : fields.Raw(default=None)
}

class APIResponse(object):

    def __init__(self, code=0, message="", data=None):
        if not message:
            message = MESSAGE.get(code)
        data = field_to_json(data)
        self.code = code
        self.message = message
        self.data = data