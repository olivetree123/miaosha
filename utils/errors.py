class NotEnough(Exception):
    def __init__(self, message="resource not enough"):
        super().__init__(self, message)


class ParamError(Exception):
    def __init__(self, message="param error"):
        super().__init__(self, message)