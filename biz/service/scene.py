"""
scene service
负责执行scene相关的具体业务逻辑
"""
import logging

from biz.infra.entity.scene.scene import Scene
from biz.infra.exception.biz_exception import BizException as BE
from biz.infra.exception.error_code import ErrorCode
from biz.infra.util import param_util


def scene_create(data):
    """
    创建scene
    :param data:
    :return:
    """
    # 提取参数
    name = param_util.require_param("name", data)
    agents = param_util.require_param("agents", data)
    try:
        # 创建一个场景
        scene = Scene(name=name, agents=agents)
    except Exception as e:
        # 异常处理
        logging.error(e)
        raise BE.error(ErrorCode.DB_CREATE_FAILED)
    return scene


def scene_delete(data):
    # 提取参数
    oid = param_util.require_param("id", data)
    try:
        # 查询场景
        scene = Scene.objects.get(id=oid)
        # 删除场景
        scene.delete()
    except Exception as e:
        logging.error(e)
        raise BE.error(ErrorCode.DB_DELETE_FAILED)


def scene_update(data):
    oid = param_util.require_param("id", data)
    name = param_util.try_param("name", data)
    agents = param_util.require_param("agents", data)
    try:
        scene = Scene.objects.get(id=oid)
        scene.name = name if name else scene.name
        scene.agents = agents
    except Exception as e:
        logging.error(e)
        raise BE.error(ErrorCode.DB_UPDATE_FAILED)
    return scene


def scene_list(data):
    page = param_util.try_param("page", data, 1)
    limit = param_util.try_param("limit", data, 10)
    offset = (page - 1) * limit
    try:
        scenes = Scene.objects.skip(offset).limit(limit)
        total = scenes.count()
        scenes = [scene.to_dict() for scene in scenes]
        return {
            "total": total,
            "scenes": scenes,
        }
    except Exception as e:
        logging.error(e)
        raise BE.error(ErrorCode.DB_NOT_FOUND)


def scene_get(data):
    oid = param_util.require_param("id", data)
    try:
        scene = Scene.objects.get(id=oid)
        return scene
    except Exception as e:
        logging.error(e)
        raise BE.error(ErrorCode.DB_NOT_FOUND)
