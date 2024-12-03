from mongoengine import StringField

from entity.agent.agent import Agent

"""
Judge 判断者
根据身份设定，任务和文本输入，输出对于情况的判断
"""


class Judge(Agent):
    identity_setting = StringField()
    task = StringField()
    output = StringField()
