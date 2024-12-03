from entity.agent.agent import Agent

"""
Handler 处理者
将judge的输出作为输入，并执行deal对应的处理程序
"""


class Handler(Agent):
    def __init__(self, name, description, avatar, deal):
        super().__init__(name, description, avatar, )
        self.deal = deal  # Hook的处理程序
