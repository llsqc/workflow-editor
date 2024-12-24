"""
Analyser 分析者
根据用户设定和task得到长文本输出
"""
import json

from mongoengine import StringField

from biz.infra.entity.agent.agent import Agent
from biz.infra.util import LLM

"""
Analyser 分析者
根据用户设定和task得到长文本输出
"""


class Analyser(Agent):
    identity_setting = StringField()
    task = StringField()

    def call(self, text, stream=False):
        """
        调用分析者进行文本分析
        :param text: 输入的文本
        :param stream: 是否以流式方式返回结果
        :return: 包含分析结果的生成器
        """
        prompts = self.generate_prompts(text)
        result = LLM.call_chat(self.identity_setting, prompts, stream)

        def generator():
            if not stream:
                yield json.dumps({
                    "number": 0,
                    "id": str(self.id),
                    "content": result
                }, ensure_ascii=False) + '\n'
            else:
                i = 0
                for chunk in result:
                    yield json.dumps({
                        "number": i,
                        "id": str(self.id),
                        "content": chunk
                    }, ensure_ascii=False) + '\n'
                    i += 1

        return generator()

    def generate_prompts(self, text):
        """
        生成提示语
        :param text: 输入的文本
        :return: 提示语字符串
        """
        role = f"请记住你的身份是{self.identity_setting}"
        assign = f"你需要根据如上身份对 {text} 做出详细的分析，完成如下任务: {self.task}"
        return f"{role}\n{assign}\n记住不能使用markdown的形式输出，要求就是正常文本"

    def to_dict(self):
        """
        将分析者对象转换为字典
        :return: 包含所有字段的字典
        """
        return {
            "id": str(self.id),
            "name": self.name,
            "description": self.description,
            "avatar": self.avatar,
            "kind": self.kind,
            "identity_setting": self.identity_setting,
            "task": self.task
        }
