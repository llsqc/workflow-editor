from mongoengine import Document, StringField

"""
agent父类，定义了name，description，avatar的基本属性
"""


class Agent(Document):
    name = StringField()
    description = StringField()
    avatar = StringField()
