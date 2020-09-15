import uuid
import hashlib
from decimal import Decimal
from datetime import date, datetime
from peewee import Model, ModelSelect


DATE_FORMAT = "%Y-%m-%d"
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

def content_md5(content):
    hash_md5 = hashlib.md5(content)
    return hash_md5.hexdigest()

def file_md5(f):
    hash_md5 = hashlib.md5()
    for chunk in iter(lambda: f.read(4096), b""):
        hash_md5.update(chunk)
    return hash_md5.hexdigest()

def date_to_str(_date):
    return _date.strftime(DATE_FORMAT)

def datetime_to_str(_datetime, _format=DATETIME_FORMAT):
    return _datetime.strftime(_format)

def str_to_datetime(time_str, _format=DATETIME_FORMAT):
    if not time_str:
        return None
    try:
        r = datetime.strptime(time_str, _format)
    except Exception as e:
        print(e)
        return None
    return r

def field_to_json(value):
    ret = value
    if isinstance(value, datetime):
        ret = datetime_to_str(value)
    elif isinstance(value, date):
        ret = date_to_str(value)
    elif isinstance(value, list):
        ret = [field_to_json(_) for _ in value]
    elif isinstance(value, dict):
        ret = {k: field_to_json(v) for k, v in value.items()}
    elif isinstance(value, bytes):
        ret = value.decode("utf-8")
    elif isinstance(value, bool):
        ret = int(ret)
    elif isinstance(value, uuid.UUID):
        ret = str(value)
    elif isinstance(value, Decimal):
        ret = float(ret)
    elif isinstance(value, ModelSelect):
        ret = [field_to_json(_) for _ in value]
    elif isinstance(value, Model):
        ret = value.to_json()
    return ret

def str_to_int(value):
    if isinstance(value, int):
        return value
    if isinstance(value, (bytes, str)):
        assert value.isdigit()
        return int(value)
    # raise Exception("Can not convert {} to int".format(value))
    return None
