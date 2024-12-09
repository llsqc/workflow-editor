from mongoengine import StringField

from entity.agent.agent import Agent

"""
Handler 处理者
将judge的输出作为输入，并执行deal对应的处理程序
"""


class Handler(Agent):
    deal = StringField()

    def handle(self, text):
        try:
            local_vars = {'text': text}
            exec(self.deal, {}, local_vars)
            result = local_vars.get('result', None)
        except Exception as e:
            return f"Handler: {self.name} 执行失败，错误信息: {e}"
        return f"Handler: {self.name} 执行成功, 输出如下: {result}" if result is not None else f"Handler: {self.name} 执行成功"

    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "avatar": self.avatar,
            "kind": self.kind,
            "deal": self.deal
        }


if __name__ == '__main__':
    class H:
        def __init__(self, name, deal):
            self.name = name
            self.deal = deal

        def handle(self, text):
            try:
                local_vars = {'text': text}
                exec(self.deal, {}, local_vars)
                result = local_vars.get('result', None)
            except Exception as e:
                return f"Handler: {self.name} 执行失败，错误信息: {e}"
            return f"Handler: {self.name} 执行成功, 输出如下: {result}" if result is not None else f"Handler: {self.name} 执行成功"


    h = H("test", """
if text == "是":
    result = "对对对"
else:
    result = "错错错"
""")

    print(h.handle("错"))
