from datetime import datetime

from mongoengine import Document, StringField, ListField, DateTimeField

from biz.infra.entity.response import Response
from biz.service.call import get_agent


class Scene(Document, Response):
    """
    场景类，继承自mongoengine的Document和Response类。
    表示一个场景，包含场景名称、agent列表、创建时间和更新时间等属性。
    """

    # 场景名称
    name = StringField()
    # agent列表，存储agent的ID
    agents = ListField(StringField())
    # 创建时间，默认为当前时间
    create_time = DateTimeField(default=datetime.now)
    # 更新时间，默认为当前时间
    update_time = DateTimeField(default=datetime.now)

    def to_dict(self):
        """
        将Scene对象转换为字典格式，以便于序列化和传输。

        Returns:
            dict: 包含场景详细信息的字典，包括id、name、agents、create_time和 update_time。
        """
        # 初始化一个空列表，用于存储agent的详细信息
        agents_list = []
        # 遍历agent ID列表，获取每个agent的详细信息并转换为字典格式
        for agent_id in self.agents:
            agents_list.append(get_agent(agent_id).to_dict())

        # 返回一个字典，包含场景的详细信息
        return {
            'id': str(self.id),  # 场景的唯一标识符
            'name': self.name,  # 场景名称
            'agents': agents_list,  # agent的详细信息列表
            'create_time': self.create_time.isoformat(),  # 创建时间的ISO格式字符串
            'update_time': self.update_time.isoformat(),  # 更新时间的ISO格式字符串
        }
