"""
call agent调用controller
"""
import types

from flask import Blueprint, request, stream_with_context, Response

from service import call as callService
from util import responseUtil

bp = Blueprint('call', __name__,url_prefix='/call')


@bp.route('/one', methods=['POST'])
def call():
    """
    调用agent函数
    """
    data = request.get_json()
    try:
        result = callService.call(data)
    except Exception as e:
        return responseUtil.fail(e)
    else:
        if isinstance(result, types.GeneratorType):
            return Response(stream_with_context(result))
        else:
            return responseUtil.succeed(result)
