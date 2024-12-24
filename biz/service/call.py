from biz.infra.entity.agent.agent import Agent


def call(data):
    """
    调用AI实现agent功能
    """

    # 输入处理 并 获取对应的agent
    oid = data['id']  # agent的id
    text = data['input']  # 输入
    agent = get_agent(oid)

    result = agent.call(text=text, stream=True)

    return result


def get_agent(oid):
    """
    根据oid获取对应的agent
    """
    query = {'id': oid}
    return Agent.objects.get(**query)
