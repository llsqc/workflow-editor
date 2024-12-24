from flask import jsonify

from entity.response import Response
from exception.biz_exception import BizException

"""
an util to serialise the Response to json
if the payload is instance of the custom Response will call to_dict for serialization
else the payload will call jsonify directly
"""


def succeed(payload, code=0, msg="success"):
    if isinstance(payload, Response):
        return jsonify({"code": code, "msg": msg, "payload": payload.to_dict()})
    else:
        return jsonify({"code": code, "msg": msg, "payload": payload})


def fail(payload, code=999, msg="unknown error"):
    if isinstance(payload, Response):
        return jsonify({"code": code, "msg": msg, "payload": payload.to_dict()})
    elif isinstance(payload, BizException):
        return jsonify({"code": code, "msg": msg, "payload": payload.to_dict()})
    elif isinstance(payload, Exception):
        return jsonify({"code": code, "msg": msg, "payload": payload.args[0]})
    else:
        return jsonify({"code": code, "msg": msg, "payload": payload})
