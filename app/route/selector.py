"""
selector对应于前端页面的selector概念，指定位到一个具体的layout所需要的参数，这里就是：
namespace, scene, scope, layout

这里定义了关于selector的 CROD
"""
from flask import json, request

from . import main
from .base import jsonify_wrapper, clear_all
from ..model import EhCommunities, EhRegions, EhUsers, EhOrganizations
from ..model import EhItemServiceCategries
from ..model import EhLaunchPadLayouts, EhNamespaces
from ..model import EhNamespaceDetails
from .. import db


# namespace列表数据
@main.route("/api/getNsList", methods=['POST'])
@jsonify_wrapper
def get_ns_list():
    """
    取得全局的域空间列表

    POST /api/getNsList

    input:

       null

    output:

    .. code-block:: javascript

       {
         "nslist": [
           {
             "id": ns.id,
             "name": ns.name
           }
         ]
       }
    """
    nslist = map(lambda ns: {'id': ns.id, 'name': ns.name},
                 EhNamespaces.query.all())
    return {'nslist': list(nslist)}


@main.route("/api/getSceneList", methods=['POST'])
@jsonify_wrapper
def get_scene_list():
    """
    取得当前域空间下的scene列表

    一个域空间可以分做小区和园区，具体的标识由eh_namespace_detials表给出

    在eh_namespace_detials表中，某一个namespace_id对应的resource_type有三种值

       * community_mix
       * community_residential
       * community_commercial

    community_commercial 为园区类型，scene_list为[ 管理员， 园区游客 ]

    其它值 为小区类型，返回[ 管理员， 小区游客 ]

    左邻域 namespace_id = 0 是特殊情况，需要返回全部的三种类型

    三种类型的对应值如下：

    .. code-block:: javascript

       {
         'default': '小区游客',
         'pm_admin': '管理员',
         'park_tourist': '园区游客'
       }

    POST /api/getSceneList

    input:

    .. code-block:: javascript

        { "ns": 999992 }

    output:

    .. code-block:: javascript

       {
         "scenelist": [
             'pm_admin', 'park_tourist'
         ]
       }
    """
    ns = request.get_json().get('ns')
    if ns == 0:
        return {'scenelist': ['pm_admin', 'park_tourist', 'default']}

    details = EhNamespaceDetails.query.filter_by(namespace_id=ns).all()
    scenelist = ['pm_admin']
    if details[0].resource_type == 'community_commercial':
        scenelist.append('park_tourist')
    else:
        scenelist.append('default')
    return {'scenelist': scenelist}


def query_category_list(ns, scene):
    dblist = EhItemServiceCategries.query \
        .filter_by(namespace_id=ns, scene_type=scene) \
        .order_by('order').all()
    categorylist = map(lambda c: dict(id=c.id, name=c.name), dblist)
    return list(categorylist)


@main.route("/api/getCategoryList", methods=['POST'])
@jsonify_wrapper
def get_category_list():
    """
    取得当前的分类列表

    这里的分类列表数据来自eh_item_service_categries（不是categories，你没有看错！！！）

    分类列表的作用在于，对Navigator widget中的全部item进行分类管理，当点击全部类型的item之后，
    会进入一个新的页面，按照分类呈现出所有的item

    POST /api/getCategoryList

    input:

    .. code-block:: javascript

       {
         "ns": 999992,
         "scene": "pm_admin"
       }

    output:

    返回的数组列表按照order字段升序排列

    .. code-block:: javascript

       {
         "categorylist": [
           {
             "id": "8",
             "name": "园区运营服务"
           }
         ]
       }
    """
    param = request.get_json()
    ns = param.get('ns')
    scene = param.get('scene')

    return dict(categorylist=query_category_list(ns, scene))


@main.route("/api/addCategory", methods=['POST'])
@jsonify_wrapper
def add_category():
    """
    在当前 ns, scene 下，新增一个category

    这里有一个细节，新增加的category，其order字段是在已有条件下所有categories数据中最大的
    order基础上增加1

    POST /api/addCategory

    input:

    .. code-block:: javascript

       {
         "ns": 999992,
         "scene": "pm_admin",
         "name": "企业行政服务"
       }

    output:

    返回的插入新数据后的数组，列表按照order字段升序排列

    .. code-block:: javascript

       {
         "categorylist": [
           {
             "id": "8",
             "name": "园区运营服务"
           }, {
             "id": "9",
             "name": "企业行政服务"
           }
         ]
       }
    """
    param = request.get_json()
    ns = param.get('ns')
    name = param.get('name')
    scene = param.get('scene')

    data = EhItemServiceCategries.query.filter_by(namespace_id=ns, scene_type=scene).all()
    if len(data) == 0:
        order = 1
    else:
        orders = map(lambda c: c.order, data)
        order = max(orders) + 1

    category_row = EhItemServiceCategries(namespace_id=ns, name=name, scene_type=scene, order=order)
    db.session.add(category_row)
    db.session.commit()

    return dict(categorylist=query_category_list(ns, scene))


@main.route("/api/delCategory", methods=['POST'])
@jsonify_wrapper
def del_category():
    """
    删除一个分类

    POST /api/delCategory

    input:

    .. code-block:: javascript

       {
         "ns": 999992,
         "scene": "pm_admin",
         "id": 9
       }

    output:

    返回的删除数据后的数组，列表按照order字段升序排列

    .. code-block:: javascript

       {
         "categorylist": [
           {
             "id": "8",
             "name": "园区运营服务"
           }
         ]
       }
    """
    param = request.get_json()
    ns = param.get('ns')
    scene = param.get('scene')
    id = param.get('id')

    EhItemServiceCategries.query.filter_by(id=id).delete()
    db.session.commit()

    return dict(categorylist=query_category_list(ns, scene))


# code: 0 全部 1 小区 2 城市 3 用户 4 机构
scope_code_enum = dict(ALL=0, COMMUNITY=1, CITY=2, USER=3, ORGANIZATION=4)


def query_scope_list(ns, scene):
    layoutlist = EhLaunchPadLayouts.query.filter_by(namespace_id=ns, scene_type=scene).all()
    duplist = map(lambda l: dict(id=l.scope_id, code=l.scope_code), layoutlist)
    # build a temp dict and unique a list of dict
    uniquelist = list({d['id']:d for d in duplist}.values())
    for scope in uniquelist:
        id = scope.get('id')
        code = scope.get('code')

        if code == scope_code_enum.get('ALL'):
            scope['name'] = '全部'
        elif code == scope_code_enum.get('COMMUNITY'):
            scope['name'] = EhCommunities.query.filter_by(id=id).one().name
        elif code == scope_code_enum.get('CITY'):
            # level = 2 means it's a city
            scope['name'] = EhRegions.query.filter_by(id=id, level=2).one().name
        elif code == scope_code_enum.get('USER'):
            scope['name'] = EhUsers.query.filter_by(id=id).one().nick_name
        elif code == scope_code_enum.get('ORGANIZATION'):
            scope['name'] = EhOrganizations.query.filter_by(id=id).one().name

    return uniquelist


@main.route("/api/getUsedScopeList", methods=['POST'])
@jsonify_wrapper
def get_used_scope_list():
    """
    取得当前的scope列表

    后台的数据库中存储有很多scope，这个接口只是获取当前所有的layout,item数据中已使用的scope

    关于scope，有5种类型，由scope.code来区分

    .. code-block:: javascript

       {
         0: "全部",
         1: "小区",
         2: "城市",
         3: "用户",
         4: "机构",
       }

    * 0, 全部，不关联数据表，对应的id是0,名称是 "全部"
    * 1, 小区，从eh_communities表取数据，id对应表的id，名称取表的name字段
    * 2, 城市，从eh_Regions表取数据，其中城市数据由字段level=2进行过滤;id对应表的id，名称取表的name字段
    * 3, 用户，从eh_users表取数据，id对应表的id，名称取表的nick_name字段
    * 4, 机构，从eh_organizations表取数据，id对应表的id，名称取表的name字段

    POST /api/getUsedScopeList

    input:

    .. code-block:: javascript

       {
         "ns": 999992,
         "scene": "pm_admin"
       }

    output:

    .. code-block:: javascript

       {
         "scopelist": [
           {
             "id": 0,
             "code": 0,
             "name": "全部"
           }
         ]
       }
    """
    param = request.get_json()
    ns = param.get('ns')
    scene = param.get('scene')

    return dict(scopelist=query_scope_list(ns, scene))


@main.route("/api/getScopeName", methods=['POST'])
@jsonify_wrapper
def get_scope_name():
    """
    取得相应code id对应的scope的名称

    用于前端要在当前layout增加关联一个新的scope的时候，进行异步的搜索查询，方便前端的输入

    POST /api/getScopeName

    input:

    .. code-block:: javascript

       {
         "ns": 999992,
         "code": 0,
         "id": 0,
       }

    output:

    .. code-block:: javascript

       {
         "name": "全部"
       }
    """
    param = request.get_json()
    ns = param.get('ns')
    code = param.get('code')
    id = param.get('id')

    name = ''
    if code == scope_code_enum.get('ALL'):
        name = '全部'
    elif code == scope_code_enum.get('COMMUNITY'):
        data = EhCommunities.query.filter_by(namespace_id=ns, id=id).all()
        name = data[0].name if len(data) != 0 else ''
    elif code == scope_code_enum.get('CITY'):
        # level = 2 means it's a city
        data = EhRegions.query.filter_by(namespace_id=ns, level=2, id=id).all()
        name = data[0].name if len(data) != 0 else ''
    elif code == scope_code_enum.get('USER'):
        data = EhUsers.query.filter_by(namespace_id=ns, id=id).all()
        name = data[0].nick_name if len(data) != 0 else ''
    elif code == scope_code_enum.get('ORGANIZATION'):
        data = EhOrganizations.query.filter_by(namespace_id=ns, id=id).all()
        name = data[0].name if len(data) != 0 else ''

    return dict(name=name)


@main.route("/api/delScope", methods=['POST'])
@jsonify_wrapper
def del_scope():
    """
    删除一个关联的scope

    注意，这里和category的删除不同，category的删除只是删除了一个分类数据而已，但是scope的删除需要连带将
    所有在此 ns>scene>scope 下建立的所有 layout item 数据全部删除

    另，在前端做了限制，scope 0是不可以删除的，所以理论上这里不会接收到id=0的值

    POST /api/delScope

    input:

    .. code-block:: javascript

       {
         "ns": 999992,
         "scene": "pm_admin"
         "scope_code": 1,
         "scope_id": 14411
       }

    output:

    返回删除后的scope列表

    .. code-block:: javascript

       {
         "scopelist": [
           {
             "id": 0,
             "code": 0,
             "name": "全部"
           }
         ]
       }
    """
    param = request.get_json()
    ns = param.get('ns')
    scene = param.get('scene')
    scope_code = param.get('scope_code')
    scope_id = param.get('scope_id')
    # 这里layouts为数组, layout_name
    layouts = query_layout_list(ns, scene, scope_code, scope_id)

    for layout in layouts:
        clear_all(ns, scene, scope_code, scope_id, layout.get('layout_name'))

    return dict(scopelist=query_scope_list(ns, scene))


def query_layout_list(ns, scene, scope_code, scope_id):
    dblist = EhLaunchPadLayouts.query \
        .filter_by(namespace_id=ns, scene_type=scene, scope_code=scope_code, scope_id=scope_id) \
        .all()
    layout_list = map(lambda l: dict(id=l.id, layout=l.name, displayName=json.loads(l.layout_json).get('displayName')), dblist)
    return list(layout_list)


@main.route("/api/getUsedLayoutList", methods=['POST'])
@jsonify_wrapper
def get_used_layout_list():
    """
    取得当前selector条件下所有的layout

    在固定的ns scene scope_code scope_id的条件下，可以建立多个layout，并且layout之前可以由item建立跳转关系
    这个接口取得所有已建立的layout

    POST /api/getUsedLayoutList

    input:

    .. code-block:: javascript

       {
         "ns": 999992,
         "scene": "pm_admin",
         "scope_code": 0,
         "scope_id": 0
       }

    output:

    .. code-block:: javascript

       {
         "layoutlist": [
           {
             "id": 14270,
             "layout": "ServiceMarketLayout",
             "displayName": "服务市场"
           }
         ]
       }
    """
    param = request.get_json()
    ns = param.get('ns')
    scene = param.get('scene')
    scope_code = param.get('scope_code')
    scope_id = param.get('scope_id')

    return dict(layoutlist=query_layout_list(ns, scene, scope_code, scope_id))


@main.route("/api/delLayout", methods=['POST'])
@jsonify_wrapper
def del_layout():
    """
    删除layout

    和删除scope类似，不过这里针对性的删除了指定的layout及其内部的item，删除scope则
    删除了所有与scope相关的所有layout及item

    同样的，在这里前端做了限制，不会对layout="ServiceMarketLayout"的服务市场进行删除，理论上
    这里不会遇到layout="ServiceMarketLayout"

    注意：后台没有addLayout的接口，这是因为在前端增加一个layout只是操作了本地的redux store，并没有
    实际的实时存储到数据库，存储的过程发生在Save接口，参考 app.route.layout.Save

    POST /api/delLayout

    input:

    .. code-block:: javascript

       {
         "ns": 999992,
         "scene": "pm_admin",
         "scope_code": 0,
         "scope_id": 0,
         "layout_name": "Pm"
       }

    output:

    返回删除后的列表数据

    .. code-block:: javascript

       {
         "layoutlist": [
           {
             "id": 14270,
             "layout": "ServiceMarketLayout",
             "displayName": "服务市场"
           }
         ]
       }
    """
    param = request.get_json()
    namespace_id = param.get('ns')
    scene_type = param.get('scene')
    scope_code = param.get('scope_code')
    scope_id = param.get('scope_id')
    layout_name = param.get('layout_name')

    clear_all(namespace_id, scene_type, scope_code, scope_id, layout_name)

    return dict(layoutlist=query_layout_list(namespace_id, scene_type, scope_code, scope_id))






