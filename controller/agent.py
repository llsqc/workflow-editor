from flask import Blueprint, request

from service import agent
from util import responseUtil

"""
agent管理controller
"""

bp = Blueprint('agent', __name__,url_prefix='/agent')


@bp.route('/create', methods=['POST'])
def agent_create():
    """
    创建agent请求
    req: name, description, avatar, type
    """
    data = request.get_json()
    try:
        result = agent.create_agent(data)
    except Exception as e:
        return responseUtil.fail(e)
    else:
        return responseUtil.succeed(result)


@bp.route('/update', methods=['POST'])
def agent_update():
    """
    更新agent配置
    """
    data = request.get_json()
    try:
        result = agent.update_agent(data)
    except Exception as e:
        return responseUtil.fail(e)
    else:
        return responseUtil.succeed(result)


@bp.route('/delete', methods=['GET'])
def agent_delete():
    """
    删除agent
    """
    oid = request.args.get('id')
    try:
        result = agent.delete_agent(oid)
    except Exception as e:
        return responseUtil.fail(e)
    else:
        return responseUtil.succeed(result)


@bp.route('/list', methods=['GET'])
def agent_list():
    """
    获取agent列表
    """
    kind = request.args.get('kind')
    try:
        result = agent.get_agents(kind)
    except Exception as e:
        return responseUtil.fail(e)
    else:
        return responseUtil.succeed(result)
