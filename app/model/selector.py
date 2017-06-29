"""
selector相应的ORM
"""
from sqlalchemy import Column
from sqlalchemy.dialects.mysql import TINYINT, INTEGER, BIGINT, DOUBLE
from sqlalchemy.dialects.mysql import VARCHAR, DATETIME, TEXT
from sqlalchemy.sql.expression import func

from .. import db


class EhNamespaces(db.Model):
    """
    eh_namespaces表
    """
    id = Column(INTEGER, primary_key=True, nullable=False, autoincrement=True)
    name = Column(VARCHAR(64), default=None)

    def __init__(self, *args, **kwargs):
        pass


class EhNamespaceDetails(db.Model):
    """
    eh_namespace_details表
    """
    id = Column(BIGINT, primary_key=True, nullable=False)
    namespace_id = Column(INTEGER, nullable=False, default='0')
    resource_type = Column(VARCHAR(128), nullable=False, default='')
    create_time = Column(DATETIME, default=None)

    def __init__(self, *args, **kwargs):
        pass


class EhItemServiceCategries(db.Model):
    """
    eh_item_service_categries表
    """
    id = Column(BIGINT, primary_key=True, nullable=False, autoincrement=True)
    name = Column(VARCHAR(64), nullable=False)
    icon_uri = Column(VARCHAR(1024), default='NULL')
    order = Column(INTEGER, default='NULL')
    align = Column(TINYINT, default='0')
    status = Column(TINYINT, nullable=False, default='1')
    namespace_id = Column(INTEGER, default='NULL')
    scene_type = Column(VARCHAR(64), nullable=False, default='default')

    def __init__(self, *args, **kwargs):
        """
        实例化EhItemServiceCategries对象

        kwargs:

        .. code-block:: javascript

           {
             "namespace_id": 999992,
             "name": "园区运营服务",
             "scene_type": "pm_admin",
             "order": 3
           }
        """
        self.namespace_id = kwargs.get('namespace_id')
        self.name = kwargs.get('name')
        self.scene_type = kwargs.get('scene_type')
        self.order = kwargs.get('order')

        max_id = EhItemServiceCategries.query.session.query(func.max(EhItemServiceCategries.id)).first()[0]

        # default value below
        self.icon_uri = 'cs://1/image/aW1hZ2UvTVRvME9ESmxPR1pqT0dFM1pHSmpaRFkwTWpRNE16TmtaVEUwTWpRMFl6UTNaUQ'
        self.align = 0
        self.status = 1
        self.id = max_id + 1


class EhCommunities(db.Model):
    """
    eh_communities表
    """
    id = Column(BIGINT, primary_key=True, nullable=False)
    uuid = Column(VARCHAR(128), nullable=False, default='')
    city_id = Column(BIGINT, nullable=False)
    city_name = Column(VARCHAR(64), default='NULL')
    area_id = Column(BIGINT, nullable=False)
    area_name = Column(VARCHAR(64), default='NULL')
    name = Column(VARCHAR(64), default='NULL')
    alias_name = Column(VARCHAR(64), default='NULL')
    address = Column(VARCHAR(512), default='NULL')
    zipcode = Column(VARCHAR(16), default='NULL')
    description = Column(TEXT)
    detail_description = Column(TEXT)
    apt_segment1 = Column(VARCHAR(64), default='NULL')
    apt_segment2 = Column(VARCHAR(64), default='NULL')
    apt_segment3 = Column(VARCHAR(64), default='NULL')
    apt_seg1_sample = Column(VARCHAR(64), default='NULL')
    apt_seg2_sample = Column(VARCHAR(64), default='NULL')
    apt_seg3_sample = Column(VARCHAR(64), default='NULL')
    apt_count = Column(INTEGER, nullable=False, default='0')
    creator_uid = Column(BIGINT, default='NULL')
    operator_uid = Column(BIGINT, default='NULL')
    status = Column(TINYINT, nullable=False, default='2')
    create_time = Column(DATETIME, default='NULL')
    delete_time = Column(DATETIME, default='NULL')
    integral_tag1 = Column(BIGINT, default='NULL')
    integral_tag2 = Column(BIGINT, default='NULL')
    integral_tag3 = Column(BIGINT, default='NULL')
    integral_tag4 = Column(BIGINT, default='NULL')
    integral_tag5 = Column(BIGINT, default='NULL')
    string_tag1 = Column(VARCHAR(128), default='NULL')
    string_tag2 = Column(VARCHAR(128), default='NULL')
    string_tag3 = Column(VARCHAR(128), default='NULL')
    string_tag4 = Column(VARCHAR(128), default='NULL')
    string_tag5 = Column(VARCHAR(128), default='NULL')
    community_type = Column(TINYINT, nullable=False, default='0')
    default_forum_id = Column(BIGINT, nullable=False, default='1')
    feedback_forum_id = Column(BIGINT, nullable=False, default='2')
    update_time = Column(DATETIME, default='NULL')
    namespace_id = Column(INTEGER, nullable=False, default='0')
    area_size = Column(DOUBLE, default='NULL')

    def __init__(self, *args, **kwargs):
        pass

class EhRegions(db.Model):
    """
    eh_regions表
    """
    id = Column(BIGINT, primary_key=True, nullable=False, autoincrement=True)
    parent_id = Column(BIGINT, default='NULL')
    name = Column(VARCHAR(64), default='NULL')
    pinyin_name = Column(VARCHAR(64), default='NULL')
    pinyin_prefix = Column(VARCHAR(64), default='NULL')
    path = Column(VARCHAR(128), default='NULL')
    level = Column(INTEGER, nullable=False, default='0')
    scope_code = Column(TINYINT, default='NULL')
    iso_code = Column(VARCHAR(32), default='NULL')
    tel_code = Column(VARCHAR(32), default='NULL')
    status = Column(TINYINT, nullable=False, default='1')
    hot_flag = Column(TINYINT, nullable=False, default='0')
    namespace_id = Column(INTEGER, nullable=False, default='0')

    def __init__(self, *args, **kwargs):
        pass


class EhUsers(db.Model):
    """
    eh_users表
    """
    id = Column(BIGINT, primary_key=True, nullable=False)
    uuid = Column(VARCHAR(128), nullable=False, default='')
    account_name = Column(VARCHAR(64), nullable=False)
    nick_name = Column(VARCHAR(128), default='NULL')
    avatar = Column(VARCHAR(2048), default='NULL')
    status_line = Column(VARCHAR(128), default='NULL')
    status = Column(TINYINT, nullable=False, default='1')
    points = Column(INTEGER, nullable=False, default='0')
    level = Column(TINYINT, nullable=False, default='1')
    gender = Column(TINYINT, nullable=False, default='0')
    birthday = Column(DATETIME, default='NULL')
    address_id = Column(BIGINT, default='NULL')
    address = Column(VARCHAR(128), default='NULL')
    community_id = Column(BIGINT, default='NULL')
    home_town = Column(BIGINT, default='NULL')
    home_town_path = Column(VARCHAR(128), default='NULL')
    occupation = Column(VARCHAR(128), default='NULL')
    company = Column(VARCHAR(128), default='NULL')
    school = Column(VARCHAR(128), default='NULL')
    locale = Column(VARCHAR(16), default='NULL')
    invite_type = Column(TINYINT, default='NULL')
    invitor_uid = Column(BIGINT, default='NULL')
    create_time = Column(DATETIME, nullable=False)
    delete_time = Column(DATETIME, default='NULL')
    last_login_time = Column(DATETIME, default='NULL')
    last_login_ip = Column(VARCHAR(64), default='NULL')
    reg_ip = Column(VARCHAR(64), default='')
    reg_city_id = Column(BIGINT, default='0')
    reg_channel_id = Column(BIGINT, default='0')
    original_avatar = Column(VARCHAR(128), default='NULL')
    salt = Column(VARCHAR(64), default='NULL')
    password_hash = Column(VARCHAR(128), default='')
    namespace_id = Column(INTEGER, nullable=False, default='0')
    namespace_user_token = Column(VARCHAR(2048), nullable=False, default='')
    namespace_user_type = Column(VARCHAR(128), default='NULL')
    executive_tag = Column(TINYINT, default='0')
    position_tag = Column(VARCHAR(128), default='NULL')
    identity_number_tag = Column(VARCHAR(20), default='NULL')

    def __init__(self, *args, **kwargs):
        pass


class EhOrganizations(db.Model):
    """
    eh_organizations表
    """
    id = Column(BIGINT, primary_key=True, nullable=False, autoincrement=True)
    parent_id = Column(BIGINT, default='NULL')
    organization_type = Column(VARCHAR(64), default='NULL')
    name = Column(VARCHAR(128), default='NULL')
    address_id = Column(BIGINT, nullable=False, default='0')
    description = Column(TEXT)
    path = Column(VARCHAR(128), default='NULL')
    level = Column(INTEGER, nullable=False, default='0')
    status = Column(TINYINT, nullable=False, default='1')
    department_type = Column(VARCHAR(64), default='NULL')
    group_type = Column(VARCHAR(64), default='NULL')
    create_time = Column(DATETIME, default='NULL')
    update_time = Column(DATETIME, default='NULL')
    directly_enterprise_id = Column(BIGINT, nullable=False, default='0')
    namespace_id = Column(INTEGER, nullable=False, default='0')
    group_id = Column(BIGINT, default='NULL')
    integral_tag1 = Column(BIGINT, default='NULL')
    integral_tag2 = Column(BIGINT, default='NULL')
    integral_tag3 = Column(BIGINT, default='NULL')
    integral_tag4 = Column(BIGINT, default='NULL')
    integral_tag5 = Column(BIGINT, default='NULL')
    string_tag1 = Column(VARCHAR(128), default='NULL')
    string_tag2 = Column(VARCHAR(128), default='NULL')
    string_tag3 = Column(VARCHAR(128), default='NULL')
    string_tag4 = Column(VARCHAR(128), default='NULL')
    string_tag5 = Column(VARCHAR(128), default='NULL')
    show_flag = Column(TINYINT, default='1')
    namespace_organization_token = Column(VARCHAR(256), default='NULL')
    namespace_organization_type = Column(VARCHAR(128), default='NULL')
    size = Column(INTEGER, default='NULL')

    def __init__(self, *args, **kwargs):
        pass
