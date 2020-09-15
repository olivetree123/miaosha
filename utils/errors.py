class GoodsNotEnough(Exception):
    def __init__(self, message="goods not enough"):
        super().__init__(self, message)


class MoneyNotEnough(Exception):
    def __init__(self, message="money not enough"):
        super().__init__(self, message)


class ParamError(Exception):
    def __init__(self, message="param error"):
        super().__init__(self, message)


class DataNotFound(Exception):
    def __init__(self, message="data not found"):
        super().__init__(self, message)