"""
call service
处理agent的调用逻辑
"""
import logging

from mongoengine import DoesNotExist

from biz.infra.entity.agent.agent import Agent
from biz.infra.exception.biz_exception import BizException as BE
from biz.infra.exception.error_code import ErrorCode
from biz.infra.util import param_util


def call(data: dict):
    """
    调用LLM基座实现agent功能。

    Args:
        data (dict): 输入数据，包含以下字段：
            - id (str): agent的唯一标识符。
            - input (str): 输入文本。

    Returns:
        Any: agent处理后的结果。
    """
    # 输入处理并获取对应的agent
    oid = param_util.require_param('id', data)  # agent的id
    text = param_util.require_param('input', data)  # 输入

    # 根据oid获取对应的agent实例
    agent = get_agent(oid)

    # 调用agent的call方法，并开启流式输出
    result = agent.call(text=text, stream=True)

    return result


def get_agent(oid: str) -> Agent:
    """
    根据oid获取对应的agent实例。

    Args:
        oid (str): agent的唯一标识符。

    Returns:
        Agent: 对应的agent实例。

    Raises:
        DoesNotExist: 如果指定的oid不存在，则会抛出DoesNotExist异常。
    """
    # 构建查询条件
    query = {'id': oid}

    # 从数据库中获取agent实例
    try:
        agent = Agent.objects.get(**query)
        return agent
    except DoesNotExist as e:
        logging.error(e)
        raise BE.error(ErrorCode.DB_NOT_FOUND)
