"""
与layout相关的ORM
"""
import json
from copy import deepcopy
from datetime import datetime

from sqlalchemy import Column
from sqlalchemy.dialects.mysql import TINYINT, INTEGER, BIGINT
from sqlalchemy.dialects.mysql import VARCHAR, DATETIME, TEXT

from .. import db


class EhBanners(db.Model):
    """
    eh_banners表
    """
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    namespace_id = Column(INTEGER, nullable=False, default='0')
    appId = Column(BIGINT, default=None)
    banner_location = Column(VARCHAR(2048), default=None)
    banner_group = Column(VARCHAR(128), nullable=False, default='')
    scope_code = Column(TINYINT, nullable=False, default='0')
    scope_id = Column(BIGINT, default=None)
    name = Column(VARCHAR(128), default=None)
    vendor_tag = Column(VARCHAR(64), default=None)
    poster_path = Column(VARCHAR(128), default=None)
    action_type = Column(TINYINT, nullable=False, default='0')
    action_data = Column(TEXT)
    start_time = Column(DATETIME, default=None)
    end_time = Column(DATETIME, default=None)
    status = Column(TINYINT, nullable=False, default='0')
    order = Column(INTEGER, nullable=False, default='0')
    creator_uid = Column(BIGINT, nullable=False, default='0')
    create_time = Column(DATETIME, default=None)
    delete_time = Column(DATETIME, default=None)
    scene_type = Column(VARCHAR(64), default='default')
    apply_policy = Column(TINYINT, nullable=False, default='0')
    update_time = Column(DATETIME, default=None)

    def __init__(self, *args, **kwargs):
        """
        实例化EhBanners对象进行数据库存储

        kwargs:

        .. code-block:: javascript

           {
             "key": "value"
           }

        传递什么值就存储什么键值

        这里对外提供的数据就像在api数据结构描述里说的那样，相应的item对象的值存储在这里，
        其它没有提供的值在内部有一些默认值来占位替代，如appId之类

        route api并没有直接操作这个类和对象，因为EhBanners和EhLaunchPadItems本质是一样的，
        不过用不同的表来存储，内部有自定义的类EhItem来屏蔽不同，提供一致的接口
        """
        defaults = (
            ('appId', 0),
            ('scope_code', 0),
            ('scope_id', 0),
            ('status', 2),
            ('order', 10),
            ('create_time', datetime.now()),
        )
        for defKey, defVal in defaults:
            setattr(self, defKey, defVal)

        for k, v in kwargs.items():
            setattr(self, k, v)


class EhLaunchPadItems(db.Model):
    """
    eh_launch_pad_items表
    """
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    namespace_id = Column(INTEGER, nullable=False, default='0')
    app_id = Column(BIGINT, default=None)
    scope_code = Column(TINYINT, nullable=False, default='0')
    scope_id = Column(BIGINT, default=None)
    item_location = Column(VARCHAR(2048), default=None)
    item_group = Column(VARCHAR(128), nullable=False, default='')
    item_name = Column(VARCHAR(32), default=None)
    item_label = Column(VARCHAR(64), default=None)
    icon_uri = Column(VARCHAR(1024), default=None)
    item_width = Column(INTEGER, nullable=False, default='1')
    item_height = Column(INTEGER, nullable=False, default='1')
    action_type = Column(TINYINT, nullable=False, default='0')
    action_data = Column(TEXT)
    default_order = Column(INTEGER, nullable=False, default='0')
    apply_policy = Column(TINYINT, nullable=False, default='0')
    min_version = Column(BIGINT, nullable=False, default='1')
    display_flag = Column(TINYINT, nullable=False, default='0')
    display_layout = Column(VARCHAR(128), default='1')
    bgcolor = Column(INTEGER, nullable=False, default='0')
    tag = Column(VARCHAR(1024), default=None)
    target_type = Column(VARCHAR(32), default=None)
    target_id = Column(VARCHAR(64), default=None)
    delete_flag = Column(TINYINT, nullable=False, default='1')
    scene_type = Column(VARCHAR(64), nullable=False, default='default')
    scale_type = Column(TINYINT, nullable=False, default='0')
    service_categry_id = Column(BIGINT, default=None)
    more_order = Column(INTEGER, nullable=False, default='0')

    def __init__(self, *args, **kwargs):
        """
        结构同EhBanners，可参考EhBanners
        """
        defaults = (
            ('app_id', 0),
            ('scope_code', 0),
            ('scope_id', 0),
            ('display_flag', 1),
            ('display_layout', None),
            ('delete_flag', 0),
        )
        for defKey, defVal in defaults:
            setattr(self, defKey, defVal)

        for k, v in kwargs.items():
            setattr(self, k, v)


class EhItem(object):
    """
    作为banner与item的抽象层，处理两种表之间的差异
    """

    def __init__(self, *args, **kwargs):
        """
        实例化item对象，在内部按类型操作EhBanners和EhLaunchPadItems

        kwargs可参考api数据结构描述 和 app.route.layout.insert_items函数
        """
        # 由于unique_key是我们辅助用的字段，这里就不需要了
        kwargs.pop('unique_key')

        if 'action_data' in kwargs:
            orig = kwargs['action_data']
            kwargs['action_data'] = json.dumps(orig, ensure_ascii=False)

        # 根据layout_name来设置item_location
        layout_name = kwargs['layout_name']
        item_location = '/home'
        if layout_name != 'ServiceMarketLayout':
            item_location += '/'
            item_location += layout_name.replace('Layout', '')
        kwargs['item_location'] = item_location

        trans = {
            'item_name': 'name',
            'item_label': 'vendor_tag',
            'icon_uri': 'poster_path',
            'item_location': 'banner_location',
            'item_group': 'banner_group',
            'app_id': 'appId',
            'display_flag': None,
            'service_categry_id': None,
            'more_order': None,
            'default_order': None
        }
        if kwargs.get('widget_type') == 'Banners':
            for oldkey, newkey in trans.items():
                if newkey is None and oldkey in kwargs:
                    kwargs.pop(oldkey)
                if oldkey in kwargs:
                    kwargs[newkey] = kwargs.pop(oldkey)

            self.__item = EhBanners(*args, **kwargs)
        else:
            self.__item = EhLaunchPadItems(*args, **kwargs)

    def getItem(self):
        return self.__item

    @classmethod
    def query(cls, *args, **kwargs):
        """
        数据库的query操作，按widget类型分别操作EhBanners.query和EhLaunchPadItems.query，
        提供一致的查询接口
        """
        Table = EhLaunchPadItems
        # 在query之前进行一次转换
        isBanner = kwargs.pop('widget_type') == 'Banners'
        if isBanner:
            Table = EhBanners
            kwargs['banner_group'] = kwargs.pop('item_group')
            kwargs['banner_location'] = kwargs.pop('item_location')

        data = Table.query
        for key, value in kwargs.items():
            arg = {key: value}
            data = data.filter_by(**arg)

        # 在使用数据之前，将数据统一
        items = []

        # 如果是item，则用more_order进行排序
        if isBanner:
            rows = data.order_by('id').all()
        else:
            rows = data.order_by('more_order').all()

        for row in rows:
            item = dict()
            if isBanner:
                for oldkey, newkey in (('name', 'item_name'),
                                       ('vendor_tag', 'item_label'),
                                       ('poster_path', 'icon_uri')):
                    item[newkey] = getattr(row, oldkey)
            else:
                for itemKey in ('item_name', 'item_label', 'icon_uri', 'default_order',
                                'item_width', 'display_flag', 'service_categry_id'):
                    item[itemKey] = getattr(row, itemKey)

            # FIXME 使用unique_key来标识item的唯一性
            item['unique_key'] = row.id

            item['action_type'] = row.action_type
            item['action_data'] = json.loads(row.action_data or '{}')
            items.append(item)
        return items


class EhLaunchPadLayouts(db.Model):
    """
    eh_launch_pad_layouts表
    """
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    namespace_id = Column(INTEGER, nullable=False, default='0')
    name = Column(VARCHAR(32), default=None)
    layout_json = Column(TEXT)
    version_code = Column(BIGINT, nullable=False, default='0')
    min_version_code = Column(BIGINT, nullable=False, default='0')
    status = Column(TINYINT, nullable=False, default='2')
    create_time = Column(DATETIME, default=None)
    scene_type = Column(VARCHAR(64), nullable=False, default='default')
    scope_code = Column(TINYINT, nullable=False, default='0')
    scope_id = Column(BIGINT, default='0')
    apply_policy = Column(TINYINT, nullable=False, default='0')

    def __init__(self, *args, **kwargs):
        """
        实例化EhLaunchPadLayouts来进行数据库的插入

        kwargs: 具体可参考函数 app.route.layout.insert_layout
        """

        self.namespace_id = kwargs.get('namespace_id')
        self.scene_type = kwargs.get('scene_type')
        self.name = kwargs.get('layout_name')
        self.scope_code = kwargs.get('scope_code')
        self.scope_id = kwargs.get('scope_id')

        layout = deepcopy(kwargs['layout'])
        layout['layoutName'] = kwargs.get('layout_name')
        # 填充默认值
        # FIXME 暂时使用数据库设定的默认值
        now = datetime.now()
        versionCode = now.strftime('%Y%m%d%S')

        self.create_time = now
        self.version_code = versionCode

        layout['versionCode'] = versionCode
        layout['versionName'] = '3.3.0'

        for index, group in enumerate(layout['groups']):
            group['defaultOrder'] = index + 1
            group['separatorFlag'] = 0
            if group['separatorHeight'] > 0:
                group['separatorFlag'] = 1

            del group['items']

        self.layout_json = json.dumps(layout, ensure_ascii=False)

