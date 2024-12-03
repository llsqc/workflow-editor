from entity.agent.agent import Agent

"""
Judge 判断者
根据身份设定，任务和文本输入，输出对于情况的判断
"""


class Judge(Agent):
    def __init__(self, name, description, avatar, identity_setting, task, output):
        super().__init__(name, description, avatar)
        self.identity_setting = identity_setting  # 身份设定
        self.task = task  # agent任务
        self.output = output  # 输出形式
