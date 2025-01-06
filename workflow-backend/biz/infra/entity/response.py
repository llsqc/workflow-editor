"""
一个抽象类作为标准，
确保所有作为响应的返回值都可以被序列化
"""


class Response:
    def to_dict(self):
        # 抽象方法，需要在子类中实现，否则默认抛出未实现异常
        raise NotImplementedError
