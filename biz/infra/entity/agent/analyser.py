"""
Analyser 分析者
根据用户设定和task得到长文本输出
"""
import json

from mongoengine import StringField

from biz.infra.entity.agent.agent import Agent
from biz.infra.util import LLM


class Analyser(Agent):
    identity_setting = StringField()
    task = StringField()

    def call(self, text, stream=False):
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
        role = f"请记住你的身份是{self.identity_setting}"
        assign = f"你需要根据如上身份对 {text} 做出详细的分析，完成如下任务: {self.task}"
        return f"{role}\n{assign}\n记住不能使用markdown的形式输出，要求就是正常文本"

    def to_dict(self):
        return {
            "id": str(self.id),
            "name": self.name,
            "description": self.description,
            "avatar": self.avatar,
            "kind": self.kind,
            "identity_setting": self.identity_setting,
            "task": self.task
        }


if __name__ == '__main__':
    class A:
        def __init__(self, name, identity_setting, task):
            self.name = name
            self.identity_setting = identity_setting
            self.task = task

        def generate_prompts(self, text):
            role = f"请记住你的身份是{self.identity_setting}"
            assign = f"你需要根据如上身份对 {text} 做出详细的分析，完成如下任务: {self.task}"
            return f"{role}\n{assign}\n记住不能使用markdown或latex的特殊形式输出，要求只能是正常文本"


    j = A(name="分析者1号", identity_setting="数学专家", task="提供这道题目的详细解题思路")
    print(j.generate_prompts("9+9等于几"))
