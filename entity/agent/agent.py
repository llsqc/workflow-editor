from mongoengine import Document, StringField, IntField

"""
agent父类，定义了name，description，avatar的基本属性
type-0 analyser
type-1 judge
type-2 hook
"""


class Agent(Document):
    name = StringField()
    description = StringField()
    avatar = StringField()
    type = IntField()
