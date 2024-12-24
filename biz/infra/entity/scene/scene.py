from datetime import datetime

from mongoengine import Document, StringField, ListField, DateTimeField

from biz.infra.entity.response import Response
from biz.service.call import get_agent


class Scene(Document, Response):
    name = StringField()
    agents = ListField(StringField())
    create_time = DateTimeField(default=datetime.now)
    update_time = DateTimeField(default=datetime.now)

    def to_dict(self):
        agents_list = []
        for agent_id in self.agents:
            agents_list.append(get_agent(agent_id).to_dict())

        return {
            'id': self.id,
            'name': self.name,
            'agents': agents_list,
            'create_time': self.create_time.isoformat(),
            'update_time': self.update_time.isoformat(),
        }
