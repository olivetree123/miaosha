#coding:utf-8

import uuid
from datetime import datetime
from playhouse.shortcuts import model_to_dict
from peewee import MySQLDatabase, PostgresqlDatabase, Model, Field, BooleanField, DateTimeField, CharField, IntegerField

from config import MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_PORT, MYSQL_DB
from utils.functions import field_to_json

db = MySQLDatabase(MYSQL_DB,
                   host=MYSQL_HOST,
                   port=MYSQL_PORT,
                   user=MYSQL_USER,
                   password=MYSQL_PASSWORD)


class UUIDField(Field):
    field_type = "char(32)"

    def db_value(self, value):
        if not isinstance(value, (str, uuid.UUID)):
            return value
        if isinstance(value, str):
            # value = uuid.UUID(value)
            try:
                value = uuid.UUID(value)  # convert hex string to UUID
            except Exception as e:
                print("Failed to convert value {} to uuid".format(value))
        value = value.hex if isinstance(value, uuid.UUID) else str(
            value)  # convert UUID to hex string.
        return value

    def python_value(self, value):
        try:
            value = uuid.UUID(value)  # convert hex string to UUID
        except Exception as e:
            print("Failed to convert value {} to uuid".format(value))
        return value


class BaseModel(Model):
    uid = UUIDField(null=False,
                    default=uuid.uuid4,
                    unique=True,
                    help_text="uid 不是主键，但是要当做主键来用")
    is_deleted = BooleanField(default=False,
                              null=False,
                              help_text="1 delete, 0 normal")
    create_time = DateTimeField(default=datetime.now)

    class Meta:
        database = db

    @classmethod
    def get_with_uid(cls, uid):
        if not uid:
            return None
        return cls.get_or_none(cls.uid == uid, cls.is_deleted == False)

    @classmethod
    def remove(cls, uid):
        r = cls.get_with_uid(uid)
        if r:
            r.is_deleted = True
            r.save()
        return r

    @classmethod
    def _get_field_names(cls):
        return cls._meta.sorted_field_names

    @classmethod
    def _get_fields(cls):
        fields = []
        for field_name in cls.get_field_names():
            field = cls._meta.fields[field_name]
            fields.append(field)
        return fields

    @classmethod
    def verify_params(cls, **params):
        # 验证 params 中的参数，主要验证非 None 字段是否有值
        fields = cls._get_fields()
        for field in fields:
            if field.auto_increment or field.default is not None or field.null:
                continue
            if params.get(field.name) is None:
                print("{} is None".format(field.name))
                return False
            # if field.unique:
            #     r = cls.get_or_none(field==params.get(field.name))
            #     if r:
            #         print("Duplicate data, field = {}, value = {}".format(field.name, params.get(field.name)))
            #         return False
        return True

    @classmethod
    def validate(cls, **params):
        # 继承该方法，验证参数
        pass

    @classmethod
    def params_handler(cls, params):
        # Model 继承该方法，处理参数
        pass

    @classmethod
    def create_data(cls, **params):
        return cls.create(**params)

    @classmethod
    def list(cls):
        return cls.select().where(cls.is_deleted == False)

    def to_json(self):
        r = model_to_dict(self)
        # id 对使用者不可见
        r.pop("id", None)
        for k, v in r.items():
            r[k] = field_to_json(v)
        return r

    def json(self):
        return self.to_json()
