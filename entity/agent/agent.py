from mongoengine import Document, StringField, IntField

"""
agent父类，定义了name，description，avatar的基本属性
kind-0 analyser
kind-1 judge
kind-2 hook
"""


class Agent(Document):
    name = StringField()
    description = StringField()
    avatar = StringField()
    kind = IntField()
