"""
与selector相对应，这里仅关于实际layout数据的加载与保存
"""
import os
from flask import render_template
from flask import redirect, request
from flask import send_from_directory
from config import BaseConfig
from . import main
from .lib import jsonify_wrapper
from ..model import Images
from .. import db

UPLOAD_FOLDER = BaseConfig.UPLOAD_FOLDER

@main.route("/")
def index():
    # access full file list
    return render_template('index.html', files = listFiles())


def addFile(filename):
    # check if duplicate file
    files = listFiles()
    for f in files:
        if filename == f.filename:
            return

    db.session.add(Images(filename=filename))
    db.session.commit()

def delFile(id):
    fileToDelete = Images.query.filter_by(id=id).one()
    db.session.delete(fileToDelete)
    db.session.commit()

def listFiles():
    return Images.query.all()


@main.route("/api/delFile/<file_id>", methods=['GET'])
def del_file(file_id):
    delFile(file_id)
    return redirect('/')


@main.route("/api/uploadFile", methods=['POST'])
def upload_file():
    file = request.files['file']
    filename = file.filename
    file.save(os.path.join(UPLOAD_FOLDER, filename))
    addFile(filename)
    return redirect('/')


@main.route("/file/<filename>", methods=['GET'])
def serve_file(filename):
    """
    提供静态资源的访问
    """
    folder = UPLOAD_FOLDER
    path = os.path.join(folder, filename)
    if not os.path.exists(path):
        filename = 'not-exist'
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)


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
