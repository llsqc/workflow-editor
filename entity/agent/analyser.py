from entity.agent.agent import Agent

"""
Analyser 分析者
根据用户设定和task得到长文本输出
"""


class Analyser(Agent):
    def __init__(self, name, description, avatar, identity_setting, task):
        super().__init__(name, description, avatar)
        self.identity_setting = identity_setting  # 身份预设
        self.task = task  # 任务
