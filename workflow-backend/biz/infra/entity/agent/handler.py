import json

from mongoengine import StringField

from biz.infra.entity.agent.agent import Agent
from biz.infra.exception.biz_exception import BizException as BE
from biz.infra.exception.error_code import ErrorCode

"""
Handler 处理者
将 judge 的输出作为输入，并执行 deal 对应的处理程序
"""


class Handler(Agent):
    # 定义一个字符串字段，用于存储处理逻辑
    deal = StringField()

    def call(self, text, stream=False):
        """
        处理输入文本并返回结果
        :param text: 输入的文本
        :param stream: 是否以流的形式返回结果
        :return: 包含处理结果的生成器
        """
        result = self.handle(text)

        def generator():
            if stream:
                # 以 JSON 格式返回处理结果
                yield json.dumps({
                    "number": 0,
                    "id": str(self.id),
                    "content": result
                }, ensure_ascii=False) + '\n'

        return generator()

    def handle(self, text):
        """
        执行存储在 deal 字段中的处理逻辑
        :param text: 输入的文本
        :return: 处理结果的字符串表示
        """
        try:
            # 创建一个局部变量字典，并将输入文本存储在其中
            local_vars = {'text': text}
            # 执行存储在 deal 字段中的代码
            exec(self.deal, {}, local_vars)
            # 获取执行结果
            result = local_vars.get('result', None)
            # 返回处理结果
            return result
        except Exception as e:
            # 捕获并返回执行过程中发生的任何异常
            raise BE.error(ErrorCode.HANDLER_CALL_FAILED)

    def to_dict(self):
        """
        将 Handler 对象转换为字典
        :return: 包含所有字段的字典
        """
        return {
            "id": str(self.id),
            "name": self.name,
            "description": self.description,
            "avatar": self.avatar,
            "kind": self.kind,
            "deal": self.deal
        }
