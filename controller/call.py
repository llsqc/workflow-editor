"""
call agent调用controller
"""
import types

from flask import Blueprint, request, stream_with_context, Response

from service import call as call_service
from util import responseUtil

bp = Blueprint('call', __name__, url_prefix='/call')


@bp.route('/one', methods=['POST'])
def call_one():
    """
    调用单个agent函数
    """
    data = request.get_json()
    try:
        result = call_service.call(data)
    except Exception as e:
        return responseUtil.fail(e)
    else:
        if isinstance(result, types.GeneratorType):
            return Response(stream_with_context(result))
        else:
            return responseUtil.succeed(result)


@bp.route('/multiple', methods=['POST'])
def call_multiple():
    """
    调用多个agent
    将上一个agent的输出作为下一个agent的输入
    :return:
    """
