"""
call agent调用controller
"""
import types

from flask import Blueprint, request, stream_with_context, Response

from biz.service import call as call_service
from biz.infra.util import response_util

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
        return response_util.fail(e)
    else:
        if isinstance(result, types.GeneratorType):
            return Response(stream_with_context(result))
        else:
            return response_util.succeed(result)
