"""
agent父类，定义了name，description，avatar的基本属性
"""


class Agent:
    def __init__(self, name, description, avatar):
        self.name = name  # agent的姓名
        self.description = description  # agent的描述
        self.avatar = avatar  # agent的头像
