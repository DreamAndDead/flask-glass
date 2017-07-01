"""
common functions that almost all route needs
"""

from functools import wraps
from flask import jsonify

from .. import db


def jsonify_wrapper(func):
    """
    a decorator, jsonify every api return dict value.

    example:

    .. code-block:: python

       @main.route('/api/search')
       @jsonify_wrapper
       def search():
           # search db, get python object data
           # data = dict(name="david")
           return data

    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        return jsonify(func(*args, **kwargs))

    return wrapper


