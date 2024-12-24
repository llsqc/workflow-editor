from biz.infra.entity.agent.agent import Agent
from biz.infra.entity.agent.analyser import Analyser
from biz.infra.entity.agent.handler import Handler
from biz.infra.entity.agent.judge import Judge
from biz.infra.entity.agent.painter import Painter
from biz.infra.util import param_util

"""
agent service
负责执行agent相关的具体业务逻辑
"""


def agent_create(data):
    """
    创建agent

    根据前端请求的数据创建相应类型的代理，并将其保存到数据库中。

    参数:
    data (dict): 包含创建代理所需数据的字典，包括 'name', 'description', 'avatar', 'kind' 等字段。

    返回:
    str: 新创建的代理的ID字符串，如果创建失败则返回错误信息。
    """
    # 提取参数
    name = param_util.require_param("name", data)
    description = param_util.try_param("description", data)
    avatar = param_util.try_param("avatar", data)
    kind = param_util.require_param("kind", data)

    try:
        # 定义不同类型的代理类和需要的参数
        agent_classes = {
            0: (Analyser, ["identity_setting", "task"]),
            1: (Judge, ["identity_setting", "task", "output"]),
            2: (Handler, ["deal"]),
            3: (Painter, ["identity_setting", "style"])
        }

        if kind not in agent_classes:
            return "kind invalid"

        agent_class, required_fields = agent_classes[kind]
        # 检查所有必需的字段是否都存在于data中
        for field in required_fields:
            if field not in data:
                return f"Missing required field: {field}"

        # 构建参数字典
        params = {
            "name": name,
            "description": description,
            "avatar": avatar,
            "kind": kind,
        }
        # 添加类型特定的字段
        for field in required_fields:
            params[field] = data[field]

        # 创建agent实例
        agent = agent_class(**params)
        agent.save()
        return str(agent.id)
    except Exception as e:
        print(f"Error creating agent: {e}")
        return None


def agent_update(data):
    """
    更新agent信息

    根据提供的数据更新指定代理的信息。

    参数:
    data (dict): 包含更新代理所需数据的字典，包括'id', 'name', 'description', 'avatar', 'kind' 等字段，以及类型特定的字段。

    返回:
    str: 成功更新时返回"Successfully updated agent"，失败时返回错误信息。
    """
    agent_id = param_util.require_param("id", data)
    if not agent_id:
        print("Agent id is required for update")
        return "find agent failed"

    try:
        # 根据id查找Agent对象
        agent = Agent.objects.get(id=agent_id)

        # 定义公共字段和类型特定字段的映射
        common_fields = ["name", "description", "avatar", "kind"]
        kind_fields = {
            0: ["identity_setting", "task"],
            1: ["identity_setting", "task", "output"],
            2: ["deal"],
            3: ["identity_setting", "style"]
        }

        # 更新公共字段
        for field in common_fields:
            if field in data:
                setattr(agent, field, data[field])

        # 更新类型特定字段
        kind = agent.kind
        if kind in kind_fields:
            for field in kind_fields[kind]:
                if field in data:
                    setattr(agent, field, data[field])

        # 保存更新
        agent.save()
        return "Successfully updated agent"
    except Exception as e:
        print(f"Error updating agent: {e}")
        return "Error updating agent"


def agent_delete(oid):
    """
    删除agent

    根据提供的对象ID删除相应的代理。

    参数:
    oid (str): 代理的ID字符串。

    返回:
    str: 删除成功时返回None，失败时返回"Error deleting agent"。
    """
    try:
        # 根据oid查找Agent对象
        agent = Agent.objects.get(id=oid)
        # 删除对象
        agent.delete()
    except Exception as e:
        print(f"Error deleting agent: {e}")
        return "Error deleting agent"


def agent_list(kind):
    """
    获取agent列表

    根据指定的代理类型，获取并返回该类型的所有代理列表。

    参数:
    kind (int): 代理的类型标识。

    返回:
    list: 包含所有指定类型代理的字典列表，每个字典表示一个代理的详细信息，失败时返回错误信息。
    """
    try:
        # 根据kind查询Agent对象列表
        agents = Agent.objects(kind=kind)
        agents_list = []
        for agent in agents:
            agents_list.append(agent.to_dict())
        return agents_list
    except Exception as e:
        print(f"Error getting agents: {e}")
        return "Error getting agents"
