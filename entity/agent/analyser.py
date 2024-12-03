from mongoengine import StringField

from entity.agent.agent import Agent

"""
Analyser 分析者
根据用户设定和task得到长文本输出
"""


class Analyser(Agent):
    identity_setting = StringField()
    task = StringField()
