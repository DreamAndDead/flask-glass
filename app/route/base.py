"""
此文件包含 api functions 需要引用的公共部分
"""

from functools import wraps

from flask import jsonify

from .. import db
from ..model import EhBanners, EhLaunchPadItems
from ..model import EhLaunchPadLayouts


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


def name2location(name):
    """
    layout在数据库中有layout_name和layout_location两个重要的属性，这个函数用来将layout_name转化为layout_location

    首页服务市场layout_name是固定的`ServiceMarketLayout`, layout_location为`/home`

    其它的layout_name约定都是以*Layout*结尾的字符串

    转换逻辑：

    if  ServiceMarketLayout， return   /home

    if  EtcLayout,  return  /home/Etc
    """
    location = '/home'
    if name != 'ServiceMarketLayout':
        location = location + '/' + name.replace('Layout', '')
    return location


def clear_all(namespace_id, scene_type, scope_code, scope_id, layout_name):
    """
    删除某个特定selector下的所有数据（layout, widget, item）

    5个参数作为一个selector
    """
    item_location = banner_location = name2location(layout_name)

    db.session.query(EhLaunchPadLayouts).filter_by(
        namespace_id=namespace_id,
        scene_type=scene_type,
        name=layout_name,
        scope_code=scope_code,
        scope_id=scope_id
    ).delete()
    db.session.query(EhBanners).filter_by(
        namespace_id=namespace_id,
        scene_type=scene_type,
        banner_location=banner_location,
        scope_code=scope_code,
        scope_id=scope_id
    ).delete()
    db.session.query(EhLaunchPadItems).filter_by(
        namespace_id=namespace_id,
        scene_type=scene_type,
        item_location=item_location,
        scope_code=scope_code,
        scope_id=scope_id
    ).delete()
    db.session.commit()



