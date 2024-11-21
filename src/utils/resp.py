# -*- coding: utf-8 -*-
# @Time    : 2024/11/1 9:52
# @Author  : codewen77
ERROR_CODE = 400
OK_CODE = 200


class Resp:
    """
    返回对象
    """

    @classmethod
    def error(cls, error_msg: str):
        """
        返回一个错误消息
        :param cls:
        :param error_msg:
        :return:
        """
        response = Response(code=ERROR_CODE, msg=error_msg, data=None)
        return response

    @classmethod
    def ok(cls, data):
        """
        返回一个json
        :param cls:
        :param data:
        :return:
        """
        response = Response(code=OK_CODE, msg='操作成功', data=data)
        return response


class Response:
    def __init__(self, code: int, msg: str, data: object):
        if code not in [200, 400]:
            raise ValueError("Invalid code value")
        self.code = code
        self.msg = msg
        self.data = data

    def __json__(self):
        return {
            "code": self.code,
            "msg": self.msg,
            "data": self.data
        }