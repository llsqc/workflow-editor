from biz.infra.exception.biz_exception import BizException as BE
from biz.infra.exception.error_code import ErrorCode

"""
param_util 参数工具类
提供解析参数的必要工具类
"""


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


def try_param(param, data, re=None):
    """
    尝试获取参数
    若不存在则返回None
    :param param: 参数名
    :param data: 参数json
    :param re: 默认返回参数
    :return: 参数 or None
    """
    if param in data:
        return data[param]
    return re
