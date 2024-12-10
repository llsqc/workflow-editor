"""
Judge 判断者
根据身份设定，任务和文本输入，输出对于情况的判断
"""
from mongoengine import StringField, MapField

from entity.agent.agent import Agent


class Judge(Agent):
    identity_setting = StringField()
    task = StringField()
    output = MapField(StringField())

    def generate_prompts(self, text):
        role = f"请记住你的身份是{self.identity_setting}"
        assign = f"你需要根据如上身份对情况{text},完成判断任务:{self.task}"
        out = "你的回答需要根据如下要求:\n"
        for k, v in self.output.items():
            out += f"当情况{k}发生时，你需要输出{v}\n"
        out += "按照要求输出，不要有其他多余的内容"
        return f"{role}\n{assign}\n{out}"

    def to_dict(self):
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


if __name__ == '__main__':
    class J:
        def __init__(self, name, identity_setting, task, output):
            self.name = name
            self.identity_setting = identity_setting
            self.task = task
            self.output = output

        def generate_prompts(self, text):
            role = f"请记住你的身份是{self.identity_setting}"
            assign = f"你需要根据如上身份对情况{text},完成判断任务:{self.task}"
            out = "你的回答需要根据如下要求:\n"
            for k, v in self.output.items():
                out += f"当情况: {k}发生时，你需要输出{v}\n"
            out += "记住按照要求输出，不要有其他多余的内容"
            return f"{role}\n{assign}\n{out}"


    j = J(name="判断者1号", identity_setting="数学专家", task="判断是否计算正确",
          output={"计算正确": "123", "计算错误": "456"})
    print(j.generate_prompts("1+1=3"))
