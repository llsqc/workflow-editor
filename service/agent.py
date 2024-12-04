from entity.agent.agent import Agent
from entity.agent.analyser import Analyser
from entity.agent.handler import Handler
from entity.agent.judge import Judge
from entity.agent.painter import Painter


def create_agent(data):
    """
    创建对应类型的agent
    并存入数据库
    """
    name = data["name"]
    description = data["description"]
    avatar = data["avatar"]
    kind = data["kind"]
    try:
        if kind == 0:
            identity_setting = data["identity_setting"]
            task = data["task"]
            agent = Analyser(name=name, description=description, avatar=avatar, kind=kind,
                             identity_setting=identity_setting, task=task)

        elif kind == 1:
            identity_setting = data["identity_setting"]
            task = data["task"]
            output = data["output"]
            agent = Judge(name=name, description=description, avatar=avatar, kind=kind,
                          identity_setting=identity_setting, task=task, output=output)

        elif kind == 2:
            deal = data["deal"]
            agent = Handler(name=name, description=description, avatar=avatar, kind=kind, deal=deal)

        elif kind == 3:
            style = data["style"]
            agent = Painter(name=name, description=description, avatar=avatar, kind=kind, style=style)

        else:
            return "kind invalid"

        agent.save()
        return f"created agent {agent.name}"
    except Exception as e:
        print(f"Error creating agent: {e}")
        return None


def update_agent(data):
    """
    更新对应agent的信息
    """
    agent_id = data.get("id")
    if not agent_id:
        print("Agent id is required for update")
        return "find agent failed"

    try:
        # 根据id查找Agent对象
        agent = Agent.objects.get(id=agent_id)

        # 更新属性
        if "name" in data:
            agent.name = data["name"]
        if "description" in data:
            agent.description = data["description"]
        if "avatar" in data:
            agent.avatar = data["avatar"]
        if "kind" in data:
            agent.kind = data["kind"]

        # 根据kind更新特定字段
        kind = data.get("kind")
        if kind == 0:
            if "identity_setting" in data:
                agent.identity_setting = data["identity_setting"]
            if "task" in data:
                agent.task = data["task"]
        elif kind == 1:
            if "identity_setting" in data:
                agent.identity_setting = data["identity_setting"]
            if "task" in data:
                agent.task = data["task"]
            if "output" in data:
                agent.output = data["output"]
        elif kind == 2:
            if "deal" in data:
                agent.deal = data["deal"]
        elif kind == 3:
            if "style" in data:
                agent.style = data["style"]

        # 保存更新
        agent.save()
        return "Successfully updated agent"
    except Exception as e:
        print(f"Error updating agent: {e}")
        return "Error updating agent"


def delete_agent(oid):
    """
    删除agent
    """
    try:
        # 根据oid查找Agent对象
        agent = Agent.objects.get(id=oid)

        # 删除对象
        agent.delete()
        return "Successfully deleted agent"

    except Exception as e:
        print(f"Error deleting agent: {e}")
        return "Error deleting agent"


# def get_agents(kind):
#     """
#     获取agent列表
#     :param kind: 类型
#     """
#     try:
#         # 根据kind查询Agent对象列表
#         agents = Agent.objects(kind=kind)
#         # 将QuerySet转换为列表
#         agents_list = [agent.to_mongo().to_dict() for agent in agents]
#         return agents_list
#     except Exception as e:
#         print(f"Error getting agents: {e}")
#         return {"error": "Error getting agents"}

from bson import ObjectId
import json


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


def get_agents(kind):
    """
    获取agent列表
    :param kind: 类型
    """
    try:
        # 根据kind查询Agent对象列表
        agents = Agent.objects(kind=kind)

        # 将QuerySet转换为列表，并处理ObjectId
        agents_list = []
        for agent in agents:
            agent_dict = agent.to_mongo().to_dict()
            # 将ObjectId转换为字符串
            agent_dict['_id'] = str(agent_dict['_id'])
            agents_list.append(agent_dict)

        # 使用自定义的JSONEncoder序列化
        json_string = JSONEncoder().encode(agents_list)
        return json.loads(json_string)
    except Exception as e:
        print(f"Error getting agents: {e}")
        return {"error": "Error getting agents"}
