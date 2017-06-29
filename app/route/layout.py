"""
与selector相对应，这里仅关于实际layout数据的加载与保存
"""
from flask import json, request

from . import main
from .base import jsonify_wrapper, clear_all, name2location
from ..model import EhItem, EhLaunchPadLayouts
from ..model import dump
from .. import db


# 界面上的数据保存到数据库
@main.route("/api/save", methods=['POST'])
@jsonify_wrapper
def save():
    """
    保存layout的接口

    这里的数据和上述api数据结构的描述保持一致，分为selector和data，具体可参考上面

    这里的保存操作与之相关的三张表

    * eh_launch_pad_layouts
    * eh_banners
    * eh_launch_pad_items

    每次的save都会预先删除相应selector下的layout及item，再进行添加

    而且每次的save都会触发mysql导出sql文件的操作，可由路径 http://ip:host/file/*.sql来访问

    input:

    .. code-block:: javascript

        {
          "selector": {
            "ns": 999992,
            "scene": "pm_admin",
            "layout": "ServiceMarketLayout",
            "scope_id": 0,
            "scope_code": 0
          },
          "data": {
            ...
          }
        }

    output:

    .. code-block:: javascript

        {
          "status": "success"
        }
    """
    args = request.get_json()
    selector = args.get('selector')
    namespace_id = selector.get('ns')
    scene_type = selector.get('scene')
    layout_name = selector.get('layout')
    scope_code = selector.get('scope_code')
    scope_id = selector.get('scope_id')

    layout = args.get('data')

    clear_all(namespace_id, scene_type, scope_code, scope_id, layout_name)
    insert_layout(namespace_id, scene_type, layout_name, scope_code, scope_id, layout)
    insert_items(namespace_id, scene_type, layout_name, scope_code, scope_id, layout['groups'])
    # commit once, for speed up
    db.session.commit()

    # dump sql files here
    dump(ns=namespace_id)

    return {'status': 'success'}


def insert_layout(namespace_id, scene_type, layout_name, scope_code, scope_id, layout):
    """
    辅助函数，用来插入layout
    """
    # FIXME 当遇到groups数据为[]时，我们认为这个Layout是未被添加的
    # 同时也不添加任何item
    if len(layout.get('groups')) == 0:
        return
    row = EhLaunchPadLayouts(
        namespace_id=namespace_id,
        scene_type=scene_type,
        layout_name=layout_name,
        layout=layout,
        scope_code=scope_code,
        scope_id=scope_id
    )
    db.session.add(row)


def insert_items(namespace_id, scene_type, layout_name, scope_code, scope_id, groups):
    """
    辅助函数，用来插入items
    """
    for group in groups:
        widget_type = group['widget']
        item_group = group['instanceConfig']['itemGroup']
        items = group['items']

        for index, item in enumerate(items):
            row = EhItem(
                widget_type=widget_type,
                namespace_id=namespace_id,
                scene_type=scene_type,
                layout_name=layout_name,
                item_group=item_group,
                scope_code=scope_code,
                scope_id=scope_id,
                more_order=index,
                **item
            ).getItem()
            db.session.add(row)


@main.route("/api/load", methods=['POST', 'GET'])
@jsonify_wrapper
def load():
    """
    获取layout的接口

    具体结构和save保持一致，由相应的selector获得data数据

    input:

    .. code-block:: javascript

        {
          "selector": {
            "ns": 999992,
            "scene": "pm_admin",
            "layout": "ServiceMarketLayout",
            "scope_id": 0,
            "scope_code": 0
          }
        }

    output:

    .. code-block:: javascript

        {
          "data": {
            ...
          }
        }
    """
    args = request.get_json()

    namespace_id = args.get('ns')
    scene_type = args.get('scene')
    layout_name = args.get('layout')
    scope_code = args.get('scope_code')
    scope_id = args.get('scope_id')

    layout = {}
    layouts_db = EhLaunchPadLayouts.query.filter_by(
        namespace_id=namespace_id,
        scene_type=scene_type,
        name=layout_name,
        scope_code=scope_code,
        scope_id=scope_id
    ).all()
    # there will only one query in layouts_db
    for layoutDB in layouts_db:
        layout_json = json.loads(layoutDB.layout_json)
        layout['groups'] = layout_json['groups']
        layout['groups'].sort(key=lambda g: g.get('defaultOrder'))
        layout['displayName'] = layout_json['displayName']

        item_location = name2location(layout_name)

        # 添加 group 的 items
        for group in layout['groups']:
            del group['defaultOrder']
            # 如果类型是 bulletins news, 不需要对其query items
            if group['widget'] in ('Bulletins', 'News'):
                group['items'] = []
            else:
                group['items'] = query_items(namespace_id, scene_type, item_location, group, scope_code, scope_id)

    return layout


def query_items(namespace_id, scene_type, item_location, group, scope_code, scope_id):
    widget_type = group['widget']
    item_group = group['instanceConfig']['itemGroup']

    items = EhItem.query(
        widget_type=widget_type,
        namespace_id=namespace_id,
        scene_type=scene_type,
        item_location=item_location,
        item_group=item_group,
        scope_code=scope_code,
        scope_id=scope_id
    )
    return items

