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
    根据前端请求创建对应类型的agent
    并存入数据库
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
    更新对应agent的信息
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
        kind = agent.kind  # 使用代理当前的kind，或者使用data.get("kind")如果允许更新kind
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
    :param kind: 类型
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
