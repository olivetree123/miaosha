from mongoengine import (connect, Document, EmbeddedDocument, StringField,
                         DecimalField, IntField, UUIDField, ListField,
                         ReferenceField, EmbeddedDocumentField)

connect("miaosha", host="192.168.153.129", port=27017)


class Goods2(Document):
    name = StringField(required=True, max_length=200)
    price = DecimalField()
    amount = IntField()

    @classmethod
    def check_amount(cls, goods_id, amount):
        rs = cls.objects(pk=goods_id)
        if len(rs) == 0:
            raise Exception("商品不存在")
        goods = rs[0]
        if goods.amount >= amount:
            return goods
        return None


class OrderItem2(EmbeddedDocument):
    goods = ReferenceField("Goods2")
    price = DecimalField(content="成交价格")
    amount = IntField(content="成交数量")


class Order2(Document):
    user = UUIDField(required=True)
    items = ListField(EmbeddedDocumentField(OrderItem2))
