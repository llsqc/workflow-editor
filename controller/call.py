"""
call agent调用controller
"""

from flask import Blueprint, request

from service import call as callService
from util import responseUtil

bp = Blueprint('call', __name__)


@bp.route('/call', methods=['POST'])
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
        return responseUtil.succeed(result)
