from biz.infra.entity.response import Response


class BizException(Exception, Response):
    """
    BizException 业务异常类
    当运行过程中出现业务相关异常时，需要raise出对应的业务异常
    要求：code与msg强调语言，不能过于简陋，msg用英文
    该类在使用时一般通过类方法和Error来获得实例，无需手动实例化
    """

    def __init__(self, code, msg):
        super().__init__(msg)
        self.code = code
        self.msg = msg

    @classmethod
    def error(cls, error_code):
        """
        从ErrorCode枚举类创建BizException实例
        :param error_code: ErrorCode枚举类的实例
        :return: BizException 对应的业务异常类
        """
        return cls(error_code.code, error_code.msg)

    def to_dict(self):
        return {
            'code': self.code,
            'msg': self.msg,
        }
