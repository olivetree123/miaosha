BAD_REQUEST = 1000
OBJECT_SAVE_FAILED = 1001
RESOURCE_NOT_FOUND = 1002
DB_ERROR = 1003
DATA_CONFLICT = 1004
OBJECT_NOT_FOUND = 1005
WRITE_DATA_FAILED = 1006
INVALID_DATA = 1007

ACCOUNT_DUPLICATE = 1010
ACCOUNT_NOT_FOUND = 1011
LOGIN_FAILED = 1012

INVENTORY_NOT_ENOUGH = 1020

ORDER_FAILED = 1030

MESSAGE = {
    BAD_REQUEST: "参数错误",
    OBJECT_SAVE_FAILED: "对象存储失败",
    RESOURCE_NOT_FOUND: "未找到资源",
    DB_ERROR: "数据库错误",
    DATA_CONFLICT: "数据冲突",
    OBJECT_NOT_FOUND: "找不到对象",
    WRITE_DATA_FAILED: "写数据失败",
    INVALID_DATA: "数据校验失败",
    ACCOUNT_DUPLICATE: "账户已存在",
    ACCOUNT_NOT_FOUND: "账户不存在",
    LOGIN_FAILED: "账号或密码错误",
    INVENTORY_NOT_ENOUGH: "库存不足",
    ORDER_FAILED: "下单失败",
}