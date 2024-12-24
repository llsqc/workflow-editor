from enum import Enum


class ErrorCode(Enum):
    """
    ErrorCode 错误码枚举类
    业务过程中遇到并抛出的业务异常，需要在这里定义好错误码和错误信息的枚举项
    要求: 需要根据异常类别区分开
    """
    # 参数验证相关
    INVALID_PARAMETER = (999, "invalid parameter")

    # 身份验证与权限校验
    JWT_INVALID = (1000, "the JWT is in valid, please log back in")
    JWT_EXPIRED = (1001, "the JWT is expired, please log back in")
    INVALID_CODE = (1002, "the verify code is invalid")

    # 数据库相关
    DB_NOT_FOUND = (2000, "not found, please try again")
    DB_DELETE_FAILED = (2001, "delete failed, please try again")

    # 业务逻辑相关
    REGISTER_FAILED = (3000, "register failed, please try again later")
    USER_NOT_FOUND = (3001, "user not found, please register first")
    INVALID_PASSWORD = (3002, "invalid password, please enter the correct password")
    AVATAR_UPLOAD_FAILED = (3003, "avatar upload failed, please try again later")
    PASSWORD_UPDATE_FAILED = (3004, "password update failed, please try again later")
    USERNAME_UPDATE_FAILED = (3005, "user update failed, please try again later")
    EMAIL_ALREADY_REGISTERED = (3006, "email already registered, please use another email")
    INVALID_REQUEST_TYPE = (3007, "invalid request type, it must be 0 or 1")
    VERIFY_CODE_SEND_FAILED = (3008, "verify code send failed, please try again later")
    IP_NOT_EXIT = (3009, "user doesn't have ip")
    REGISTER_REPEAT = (3010, "The email address is already registered")

    UPLOAD_FAILED = (4000, "upload file failed, please try again")
    GET_IP_FAILED = (4001, "get ip failed, please try again")
    UPDATE_IP_FAILED = (4002, "update ip failed, please try again")
    RECORD_SAVE_FAILED = (4003, "workflow save failed, please try again")
    WORKFLOW_FAILED = (4004, "workflow call failed, please try again")

    def __init__(self, code, msg):
        self.code = code
        self.msg = msg
