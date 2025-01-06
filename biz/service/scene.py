"""
scene_service.py

场景服务模块，负责执行与场景（Scene）相关的具体业务逻辑。包括场景的创建、删除、更新、查询等操作。

主要功能：
- `scene_create`: 创建一个新的场景。
- `scene_delete`: 根据场景ID删除一个场景。
- `scene_update`: 更新场景的名称和代理信息。
- `scene_list`: 分页查询场景列表。
- `scene_get`: 根据场景ID获取单个场景的详细信息。
"""

import logging
from datetime import datetime

from biz.infra.entity.scene.scene import Scene
from biz.infra.exception.biz_exception import BizException as BE
from biz.infra.exception.error_code import ErrorCode
from biz.infra.util import param_util


def scene_create(data: dict) -> Scene:
    """
    创建一个新的场景。

    参数：
    - `data`: 包含创建场景所需的参数的字典，必须包含 `name` 和 `agents`。

    返回值：
    - 创建的 `Scene` 对象。

    异常处理：
    - 如果参数缺失或无效，将抛出 `BizException`，错误码为`INVALID_PARAMETER`。
    - 如果创建场景时发生数据库错误，将抛出 `BizException`，错误码为 `ErrorCode.DB_CREATE_FAILED`。
    """
    # 提取参数
    name = param_util.require_param("name", data)
    agents = param_util.require_param("agents", data)
    try:
        # 创建一个场景
        scene = Scene(name=name, agents=agents)
        scene.save()
    except Exception as e:
        # 异常处理
        logging.error(f"Failed to create scene: {e}")
        raise BE.error(ErrorCode.DB_CREATE_FAILED)
    return scene


def scene_delete(data: dict) -> dict:
    """
    根据场景ID删除一个场景。

    参数：
    - `data`: 包含场景ID的字典，必须包含 `id`。

    异常处理：
    - 如果场景ID无效或场景不存在，将抛出 `BizException`，错误码为 `ErrorCode.DB_DELETE_FAILED`。
    - 如果删除操作发生数据库错误，将抛出 `BizException`，错误码为 `ErrorCode.DB_DELETE_FAILED`。
    """
    # 提取参数
    oid = param_util.require_param("id", data)
    try:
        # 查询场景
        scene = Scene.objects.get(id=oid)
        # 删除场景
        scene.delete()
    except Exception as e:
        logging.error(f"Failed to delete scene with ID {oid}: {e}")
        raise BE.error(ErrorCode.DB_DELETE_FAILED)
    return {
        "code": 0,
        "msg": "success",
    }


def scene_update(data: dict) -> Scene:
    """
    更新场景的名称和代理信息。

    参数：
    - `data`: 包含更新场景所需参数的字典，必须包含 `id` 和 `agents`，可选包含 `name`。

    返回值：
    - 更新后的 `Scene` 对象。

    异常处理：
    - 如果场景ID无效或场景不存在，将抛出 `BizException`，错误码为 `ErrorCode.DB_UPDATE_FAILED`。
    - 如果更新操作发生数据库错误，将抛出 `BizException`，错误码为 `ErrorCode.DB_UPDATE_FAILED`。
    """
    oid = param_util.require_param("id", data)
    name = param_util.try_param("name", data)
    agents = param_util.require_param("agents", data)
    try:
        scene = Scene.objects.get(id=oid)
        scene.name = name if name else scene.name
        scene.agents = agents
        scene.update_time = datetime.now()
        scene.save()
    except Exception as e:
        logging.error(f"Failed to update scene with ID {oid}: {e}")
        raise BE.error(ErrorCode.DB_UPDATE_FAILED)
    return scene


def scene_list(data: dict) -> dict:
    """
    分页查询场景列表。

    参数：
    - `data`: 包含分页参数的字典，可选包含 `page` 和 `limit`。

    返回值：
    - 包含场景列表和总数的字典，格式为：
      ```
      {
          "total": <总场景数>,
          "scenes": [
              {
                  "id": <场景ID>,
                  "name": <场景名称>,
                  "agents": <代理列表>
              },
              ...
          ]
      }
      ```

    异常处理：
    - 如果查询操作发生数据库错误，将抛出 `BizException`，错误码为 `ErrorCode.DB_NOT_FOUND`。
    """
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
        logging.error(f"Failed to list scenes: {e}")
        raise BE.error(ErrorCode.DB_NOT_FOUND)


def scene_get(data: dict) -> Scene:
    """
    根据场景ID获取单个场景的详细信息。

    参数：
    - `data`: 包含场景ID的字典，必须包含 `id`。

    返回值：
    - 查询到的 `Scene` 对象。

    异常处理：
    - 如果场景ID无效或场景不存在，将抛出 `BizException`，错误码为 `ErrorCode.DB_NOT_FOUND`。
    """
    oid = param_util.require_param("id", data)
    try:
        scene = Scene.objects.get(id=oid)
        return scene
    except Exception as e:
        logging.error(f"Failed to get scene with ID {oid}: {e}")
        raise BE.error(ErrorCode.DB_NOT_FOUND)
