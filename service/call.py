from entity.agent.agent import Agent
from util import LLM


def call(data):
    """
    调用AI实现agent功能
    """

    # 输入处理 并 获取对应的agent
    oid = data['id']  # agent的id
    kind = data['kind']  # agent的类型
    text = data['input']  # 输入
    agent = get_agent(oid, kind)

    result = "调用失败，请重试"
    # analyser
    if kind == 0:
        prompts = agent.generate_prompts(text)
        result = LLM.call_chat(agent.identity_setting, prompts)
    # judge
    elif kind == 1:
        prompts = agent.generate_prompts(text)
        result = LLM.call_chat(agent.identity_setting, prompts)
    # handler
    elif kind == 2:
        result = agent.handle(text)

    return result


def get_agent(oid, kind):
    """
    根据oid和kind获取对应的agent
    """
    query = {'id': oid, 'kind': kind}
    return Agent.objects.get(**query)
