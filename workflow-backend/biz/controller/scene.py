"""
scene管理controller
"""
from flask import Blueprint, request

from biz.infra.util import response_util
from biz.service import scene

bp = Blueprint('scene', __name__, url_prefix='/scene')


@bp.route('/create', methods=['POST'])
def scene_create():
    """
    创建一个场景
    :return:
    """
    data = request.get_json()
    try:
        result = scene.scene_create(data)
    except Exception as e:
        return response_util.fail(e)
    else:
        return response_util.succeed(result)


@bp.route('/delete', methods=['POST'])
def scene_delete():
    """
    删除一个场景
    :return:
    """
    data = request.get_json()
    try:
        result = scene.scene_delete(data)
    except Exception as e:
        return response_util.fail(e)
    else:
        return response_util.succeed(result)


@bp.route('/update', methods=['POST'])
def scene_update():
    """
    更新一个场景
    :return:
    """
    data = request.get_json()
    try:
        result = scene.scene_update(data)
    except Exception as e:
        return response_util.fail(e)
    else:
        return response_util.succeed(result)


@bp.route('/list', methods=['POST'])
def scene_list():
    """
    获取场景列表
    :return:
    """
    data = request.get_json()
    try:
        result = scene.scene_list(data)
    except Exception as e:
        return response_util.fail(e)
    else:
        return response_util.succeed(result)


@bp.route('/get', methods=['POST'])
def scene_get():
    """
    获取场景详细信息
    :return:
    """
    data = request.get_json()
    try:
        result = scene.scene_get(data)
    except Exception as e:
        return response_util.fail(e)
    else:
        return response_util.succeed(result)
