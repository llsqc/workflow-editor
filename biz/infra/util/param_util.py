from biz.infra.exception.biz_exception import BizException as BE
from biz.infra.exception.error_code import ErrorCode


def require_param(param, data):
    """
    获取强制要求的参数
    若不存在则抛出非法参数异常
    :param param: 参数名
    :param data: 参数json
    :return: 参数 or raise
    """
    if param not in data:
        raise BE.error(ErrorCode.INVALID_PARAMETER)
    return data[param]


def try_param(param, data):
    """
    尝试获取参数
    若不存在则返回None
    :param param: 参数名
    :param data: 参数json
    :return: 参数 or None
    """
    if param in data:
        return data[param]
    return None
