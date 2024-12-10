from mongoengine import Document, StringField, IntField

from entity.response import Response

"""
agent父类，定义了name，description，avatar的基本属性
kind-0 analyser
kind-1 judge
kind-2 handler
kind-3 painter
"""


class Agent(Document, Response):
    meta = {'allow_inheritance': True}

    name = StringField()
    description = StringField()
    avatar = StringField()
    kind = IntField()

    def to_dict(self):
        return {
            "id": str(self.id),
            "name": self.name,
            "description": self.description,
            "avatar": self.avatar,
            "kind": self.kind
        }
