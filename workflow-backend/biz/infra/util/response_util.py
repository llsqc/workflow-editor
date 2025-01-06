from flask import jsonify

from biz.infra.entity.response import Response
from biz.infra.exception.biz_exception import BizException

"""
response_util 响应工具类
用于向前端返回 JSON 类型的响应。

1. 基本数据类型：
   - 使用 Flask 的 `jsonify` 默认序列化方式，将基本数据类型（如字典、列表、字符串等）直接转换为 JSON 格式。

2. 自定义类型：
   - 对于自定义类型，需继承 `biz.infra.entity.response.Response` 类，并实现 `to_dict` 方法，手动将自定义对象序列化为字典。

3. 异常处理：
   - 如果 `payload` 是一个 `BizException` 实例，调用其 `to_dict` 方法进行序列化。
   - 如果 `payload` 是一个普通的 Python `Exception` 实例，取其 `args[0]` 作为 `payload` 的值。

4. 返回格式：
   - 所有返回值均为 JSON 格式，包含以下字段：
     - `code`: 响应状态码。
     - `msg`: 响应消息。
     - `payload`: 响应的有效载荷，可以是基本数据类型、自定义对象的字典表示、或异常信息。
"""


def succeed(payload, code=0, msg="success"):
    # 继承 Response 的自定义类型
    if isinstance(payload, Response):
        return jsonify({"code": code, "msg": msg, "payload": payload.to_dict()})
    # 基本类型
    else:
        return jsonify({"code": code, "msg": msg, "payload": payload})


def fail(payload, code=999, msg="unknown error"):
    # 继承 Response 的自定义类型
    if isinstance(payload, Response):
        return jsonify({"code": code, "msg": msg, "payload": payload.to_dict()})
    # BizException 自定义异常
    elif isinstance(payload, BizException):
        return jsonify({"code": payload.code, "msg": payload.msg})
    # 内嵌异常
    elif isinstance(payload, Exception):
        return jsonify({"code": code, "msg": msg, "payload": payload.args[0]})
    # 基本类型
    else:
        return jsonify({"code": code, "msg": msg, "payload": payload})
