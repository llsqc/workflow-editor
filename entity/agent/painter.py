from mongoengine import StringField

from entity.agent.agent import Agent


class Painter(Agent):
    style = StringField()
