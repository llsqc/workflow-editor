"""
scene管理controller
"""
from flask import Blueprint

bp = Blueprint('scene', __name__, url_prefix='/scene')


@bp.route('/create', methods=('POST'))
def scene_create():
    """
    创建一个场景
    :return:
    """


@bp.route('/delete', methods=('POST'))
def scene_delete():
    """
    删除一个场景
    :return:
    """


@bp.route('/update', methods=('POST'))
def scene_update():
    """
    更新一个场景
    :return:
    """


@bp.route('/list', methods=('POST'))
def scene_list():
    """
    获取场景列表
    :return:
    """


@bp.route('/get', methods=('POST'))
def scene_get():
    """
    获取场景详细信息
    :return:
    """
