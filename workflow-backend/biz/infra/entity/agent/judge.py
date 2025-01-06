import json

from mongoengine import StringField, MapField

from biz.infra.entity.agent.agent import Agent
from biz.infra.util import LLM


class Judge(Agent):
    """
    判断者类，用于根据预设的身份、任务和输出规则，对输入的文本进行判断并生成相应的输出。
    """
    identity_setting = StringField()  # 身份设定
    task = StringField()  # 任务描述
    output = MapField(StringField())  # 输出规则

    def call(self, text, stream=False):
        """
        调用 LLM 进行判断并生成输出。

        :param text: 输入的文本
        :param stream: 是否以流式输出结果
        :return: 生成器，用于生成 JSON 格式的结果
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
        生成用于 LLM 调用的提示信息。

        :param text: 输入的文本
        :return: 提示信息字符串
        """
        role = f"请记住你的身份是{self.identity_setting}"
        assign = f"你需要根据如上身份对情况{text},完成判断任务:{self.task}"
        out = "你的回答需要根据如下要求:\n"
        for k, v in self.output.items():
            out += f"当情况{k}发生时，你需要输出{v}\n"
        out += "按照要求输出，不要有其他多余的内容"
        return f"{role}\n{assign}\n{out}"

    def to_dict(self):
        """
        将对象转换为字典格式。

        :return: 包含对象所有属性的字典
        """
        return {
            "id": str(self.id),
            "name": self.name,
            "description": self.description,
            "avatar": self.avatar,
            "kind": self.kind,
            "identity_setting": self.identity_setting,
            "task": self.task,
            "output": self.output
        }
