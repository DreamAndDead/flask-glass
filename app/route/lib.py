"""
此文件包含 api functions 需要引用的公共部分
"""

from functools import wraps
from flask import jsonify

from .. import db


def jsonify_wrapper(func):
    """
    装饰器，用于装饰每一个api，作用是将api返回的结果对象 序列为 json字符串，用于接口传输

    example:

    .. code-block:: python

       @main.route('/api/search')
       @jsonify_wrapper
       def search():
           # search db, get python object data
           # data = dict(name="zdw")
           return data

    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        return jsonify(func(*args, **kwargs))

    return wrapper


