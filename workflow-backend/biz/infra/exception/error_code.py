from enum import Enum


class ErrorCode(Enum):
    """
    ErrorCode 错误码枚举类
    业务过程中遇到并抛出的业务异常，需要在这里定义好错误码和错误信息的枚举项
    要求: 需要根据异常类别区分开
    """
    # 参数验证相关
    INVALID_PARAMETER = (999, "invalid parameter")
    MISSING_REQUIRED_FIELD = (998, "missing required field")
    UNKNOWN_FIELD = (997, "unknown field")
    MISSING_PARAMETER = (996, "missing parameter")
    DUPLICATE_PARAMETER = (995, "duplicate parameter")

    # 身份验证与权限校验
    JWT_INVALID = (1000, "the JWT is in valid, please log back in")
    JWT_EXPIRED = (1001, "the JWT is expired, please log back in")
    INVALID_CODE = (1002, "the verify code is invalid")

    # 数据库相关
    DB_NOT_FOUND = (2000, "not found, please try again")
    DB_DELETE_FAILED = (2001, "delete failed, please try again")
    DB_CREATE_FAILED = (2002, "create failed, please try again")
    DB_UPDATE_FAILED = (2003, "update failed, please try again")

    # 业务逻辑相关
    CALL_CHAT_FAILED = (3000, "call chat failed, please try again")
    HANDLER_CALL_FAILED = (3001, "handler call failed, please try again")

    def __init__(self, code, msg):
        self.code = code
        self.msg = msg
