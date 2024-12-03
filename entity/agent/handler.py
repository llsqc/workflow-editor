from mongoengine import StringField

from entity.agent.agent import Agent

"""
Handler 处理者
将judge的输出作为输入，并执行deal对应的处理程序
"""


class Handler(Agent):
    deal = StringField()
