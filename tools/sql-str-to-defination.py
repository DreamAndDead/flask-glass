#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2017 zdw <zdw@zl-zdw>
#
# Distributed under terms of the MIT license.

eh_banners = """
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT 'id of the record',
  `namespace_id` int(11) NOT NULL DEFAULT '0',
  `appId` bigint(20) DEFAULT NULL,
  `banner_location` varchar(2048) DEFAULT NULL,
  `banner_group` varchar(128) NOT NULL DEFAULT '' COMMENT 'the type to filter item when querying: GA, BIZ, PM, GARC, GANC, GAPS',
  `scope_code` tinyint(4) NOT NULL DEFAULT '0' COMMENT '0: all, 1: community, 2: city, 3: user',
  `scope_id` bigint(20) DEFAULT NULL,
  `name` varchar(128) DEFAULT NULL,
  `vendor_tag` varchar(64) DEFAULT NULL,
  `poster_path` varchar(128) DEFAULT NULL,
  `action_type` tinyint(4) NOT NULL DEFAULT '0' COMMENT 'according to document',
  `action_data` text COMMENT 'the parameters depend on item_type, json format',
  `start_time` datetime DEFAULT NULL,
  `end_time` datetime DEFAULT NULL,
  `status` tinyint(4) NOT NULL DEFAULT '0' COMMENT '0: closed, 1: waiting for confirmation, 2: active',
  `order` int(11) NOT NULL DEFAULT '0',
  `creator_uid` bigint(20) NOT NULL DEFAULT '0' COMMENT 'record creator user id',
  `create_time` datetime DEFAULT NULL,
  `delete_time` datetime DEFAULT NULL COMMENT 'mark-deletion policy, historic data may be valuable',
  `scene_type` varchar(64) DEFAULT 'default',
  `apply_policy` tinyint(4) NOT NULL DEFAULT '0' COMMENT '0: default, 1: override, 2: revert 3:customized',
  `update_time` datetime DEFAULT NULL,
"""

eh_launch_pad_items = """
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `namespace_id` int(11) NOT NULL DEFAULT '0',
  `app_id` bigint(20) DEFAULT NULL,
  `scope_code` tinyint(4) NOT NULL DEFAULT '0' COMMENT '0: all, 1: community, 2: city, 3: user',
  `scope_id` bigint(20) DEFAULT NULL,
  `item_location` varchar(2048) DEFAULT NULL,
  `item_group` varchar(128) NOT NULL DEFAULT '' COMMENT 'the type to filter item when querying: Default、GovAgencies、Bizs、GaActions',
  `item_name` varchar(32) DEFAULT NULL,
  `item_label` varchar(64) DEFAULT NULL,
  `icon_uri` varchar(1024) DEFAULT NULL,
  `item_width` int(11) NOT NULL DEFAULT '1',
  `item_height` int(11) NOT NULL DEFAULT '1',
  `action_type` tinyint(4) NOT NULL DEFAULT '0' COMMENT 'according to document',
  `action_data` text COMMENT 'the parameters depend on item_type, json format',
  `default_order` int(11) NOT NULL DEFAULT '0',
  `apply_policy` tinyint(4) NOT NULL DEFAULT '0' COMMENT '0: default, 1: override, 2: revert',
  `min_version` bigint(20) NOT NULL DEFAULT '1' COMMENT 'the min version of the item, it will be not supported if current version is less than this',
  `display_flag` tinyint(4) NOT NULL DEFAULT '0' COMMENT 'default display on the pad, 0: hide, 1:display',
  `display_layout` varchar(128) DEFAULT '1' COMMENT 'how many grids it takes at the layout, format: 2x3',
  `bgcolor` int(11) NOT NULL DEFAULT '0',
  `tag` varchar(1024) DEFAULT NULL,
  `target_type` varchar(32) DEFAULT NULL,
  `target_id` varchar(64) DEFAULT NULL COMMENT 'the entity id linked back to the orginal resource',
  `delete_flag` tinyint(4) NOT NULL DEFAULT '1' COMMENT 'whether the item can be deleted from desk, 0: no, 1: yes',
  `scene_type` varchar(64) NOT NULL DEFAULT 'default',
  `scale_type` tinyint(4) NOT NULL DEFAULT '0' COMMENT '0: 不需要, 1: 需要',
  `service_categry_id` bigint(20) DEFAULT NULL COMMENT 'service categry id',
"""

eh_launch_pad_layouts = """
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `namespace_id` int(11) NOT NULL DEFAULT '0',
  `name` varchar(32) DEFAULT NULL,
  `layout_json` text,
  `version_code` bigint(20) NOT NULL DEFAULT '0' COMMENT 'the current version code',
  `min_version_code` bigint(20) NOT NULL DEFAULT '0' COMMENT 'the minmum version code which is compatible',
  `status` tinyint(4) NOT NULL DEFAULT '2' COMMENT '0: inactive, 1: waitingForConfirmation, 2: active',
  `create_time` datetime DEFAULT NULL,
  `scene_type` varchar(64) NOT NULL DEFAULT 'default',
  `scope_code` tinyint(4) NOT NULL DEFAULT '0' COMMENT '0: all, 1: community, 2: city, 3: user',
  `scope_id` bigint(20) DEFAULT '0',
  `apply_policy` tinyint(4) NOT NULL DEFAULT '0' COMMENT '0: default, 1: override, 2: revert 3:customized',
"""

eh_namespaces = """
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'id of the record',
  `name` varchar(64) DEFAULT NULL,
"""

eh_namespace_details = """
  `id` bigint(20) NOT NULL,
  `namespace_id` int(11) NOT NULL DEFAULT '0',
  `resource_type` varchar(128) NOT NULL DEFAULT '' COMMENT 'the type of resource in the namespace, community_residential, community_commercial, community_mix',
  `create_time` datetime DEFAULT NULL,
"""

eh_item_service_categries = """
  `id` bigint(20) NOT NULL COMMENT 'id of the record',
  `name` varchar(64) NOT NULL COMMENT 'service categry name',
  `icon_uri` varchar(1024) DEFAULT NULL COMMENT 'service categry icon uri',
  `order` int(11) DEFAULT NULL COMMENT 'order ',
  `align` tinyint(4) DEFAULT '0' COMMENT '0: left, 1: center',
  `status` tinyint(4) NOT NULL DEFAULT '1' COMMENT '0: inactive, 1: active',
  `namespace_id` int(11) DEFAULT NULL,
"""

eh_communities = """
  `id` bigint(20) NOT NULL COMMENT 'id of the record',
  `uuid` varchar(128) NOT NULL DEFAULT '',
  `city_id` bigint(20) NOT NULL COMMENT 'city id in region table',
  `city_name` varchar(64) DEFAULT NULL COMMENT 'redundant for query optimization',
  `area_id` bigint(20) NOT NULL COMMENT 'area id in region table',
  `area_name` varchar(64) DEFAULT NULL COMMENT 'redundant for query optimization',
  `name` varchar(64) DEFAULT NULL,
  `alias_name` varchar(64) DEFAULT NULL,
  `address` varchar(512) DEFAULT NULL,
  `zipcode` varchar(16) DEFAULT NULL,
  `description` text,
  `detail_description` text,
  `apt_segment1` varchar(64) DEFAULT NULL,
  `apt_segment2` varchar(64) DEFAULT NULL,
  `apt_segment3` varchar(64) DEFAULT NULL,
  `apt_seg1_sample` varchar(64) DEFAULT NULL,
  `apt_seg2_sample` varchar(64) DEFAULT NULL,
  `apt_seg3_sample` varchar(64) DEFAULT NULL,
  `apt_count` int(11) NOT NULL DEFAULT '0',
  `creator_uid` bigint(20) DEFAULT NULL COMMENT 'user who suggested the creation',
  `operator_uid` bigint(20) DEFAULT NULL COMMENT 'operator uid of last operation',
  `status` tinyint(4) NOT NULL DEFAULT '2' COMMENT '0: inactive, 1: waitingForConfirmation, 2: active',
  `create_time` datetime DEFAULT NULL,
  `delete_time` datetime DEFAULT NULL COMMENT 'mark-deletion policy. historic data may be useful',
  `integral_tag1` bigint(20) DEFAULT NULL,
  `integral_tag2` bigint(20) DEFAULT NULL,
  `integral_tag3` bigint(20) DEFAULT NULL,
  `integral_tag4` bigint(20) DEFAULT NULL,
  `integral_tag5` bigint(20) DEFAULT NULL,
  `string_tag1` varchar(128) DEFAULT NULL,
  `string_tag2` varchar(128) DEFAULT NULL,
  `string_tag3` varchar(128) DEFAULT NULL,
  `string_tag4` varchar(128) DEFAULT NULL,
  `string_tag5` varchar(128) DEFAULT NULL,
  `community_type` tinyint(4) NOT NULL DEFAULT '0' COMMENT '0: residential, 1: commercial',
  `default_forum_id` bigint(20) NOT NULL DEFAULT '1' COMMENT 'the default forum for the community, forum-1 is system default forum',
  `feedback_forum_id` bigint(20) NOT NULL DEFAULT '2' COMMENT 'the default forum for the community, forum-2 is system feedback forum',
  `update_time` datetime DEFAULT NULL,
  `namespace_id` int(11) NOT NULL DEFAULT '0',
  `area_size` double DEFAULT NULL COMMENT 'area size',
"""

eh_regions = """
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT 'id of the record',
  `parent_id` bigint(20) DEFAULT NULL COMMENT 'id of the parent region',
  `name` varchar(64) DEFAULT NULL,
  `pinyin_name` varchar(64) DEFAULT NULL COMMENT 'the full pinyin of the name',
  `pinyin_prefix` varchar(64) DEFAULT NULL COMMENT 'the prefix letter of every pinyin word',
  `path` varchar(128) DEFAULT NULL COMMENT 'path from the root',
  `level` int(11) NOT NULL DEFAULT '0',
  `scope_code` tinyint(4) DEFAULT NULL COMMENT '0 : country, 1: state/province, 2: city, 3: area, 4: neighborhood (community)',
  `iso_code` varchar(32) DEFAULT NULL COMMENT 'international standard code for the region if exists',
  `tel_code` varchar(32) DEFAULT NULL COMMENT 'primary telephone area code',
  `status` tinyint(4) NOT NULL DEFAULT '1' COMMENT '1: inactive, 2: active, 3: locked, 4: mark as deleted',
  `hot_flag` tinyint(4) NOT NULL DEFAULT '0' COMMENT '0: not hot, 1: hot',
  `namespace_id` int(11) NOT NULL DEFAULT '0',
"""

eh_users = """
  `id` bigint(20) NOT NULL COMMENT 'id of the record',
  `uuid` varchar(128) NOT NULL DEFAULT '',
  `account_name` varchar(64) NOT NULL,
  `nick_name` varchar(128) DEFAULT NULL,
  `avatar` varchar(2048) DEFAULT NULL,
  `status_line` varchar(128) DEFAULT NULL COMMENT 'status line to express who you are',
  `status` tinyint(4) NOT NULL DEFAULT '1' COMMENT '0 - inactive, 1 - active',
  `points` int(11) NOT NULL DEFAULT '0' COMMENT 'points',
  `level` tinyint(4) NOT NULL DEFAULT '1',
  `gender` tinyint(4) NOT NULL DEFAULT '0' COMMENT '0: undisclosured, 1: male, 2: female',
  `birthday` date DEFAULT NULL,
  `address_id` bigint(20) DEFAULT NULL COMMENT 'current address id',
  `address` varchar(128) DEFAULT NULL COMMENT 'redundant current address description',
  `community_id` bigint(20) DEFAULT NULL COMMENT 'if current family has been setup, it is the community id from address',
  `home_town` bigint(20) DEFAULT NULL COMMENT 'region id',
  `home_town_path` varchar(128) DEFAULT NULL COMMENT 'redundant region path for recursive matching',
  `occupation` varchar(128) DEFAULT NULL,
  `company` varchar(128) DEFAULT NULL,
  `school` varchar(128) DEFAULT NULL,
  `locale` varchar(16) DEFAULT NULL COMMENT 'zh_CN, en_US etc',
  `invite_type` tinyint(4) DEFAULT NULL COMMENT '1: SMS, 2: wechat, 3, wechat friend circle, 4: weibo, 5: phone contact',
  `invitor_uid` bigint(20) DEFAULT NULL,
  `create_time` datetime NOT NULL,
  `delete_time` datetime DEFAULT NULL COMMENT 'mark-deletion policy. may be valuable for user to restore account',
  `last_login_time` datetime DEFAULT NULL,
  `last_login_ip` varchar(64) DEFAULT NULL,
  `reg_ip` varchar(64) DEFAULT '' COMMENT 'the channel at the time of register',
  `reg_city_id` bigint(20) DEFAULT '0' COMMENT 'the city at the time of register',
  `reg_channel_id` bigint(20) DEFAULT '0' COMMENT 'the channel at the time of register',
  `original_avatar` varchar(128) DEFAULT NULL COMMENT 'the path of avatar in 2.8 version, keep it for migration',
  `salt` varchar(64) DEFAULT NULL,
  `password_hash` varchar(128) DEFAULT '' COMMENT 'Note, password is stored as salted hash, salt is appended by hash together',
  `namespace_id` int(11) NOT NULL DEFAULT '0',
  `namespace_user_token` varchar(2048) NOT NULL DEFAULT '',
  `namespace_user_type` varchar(128) DEFAULT NULL COMMENT 'the type of user',
  `executive_tag` tinyint(4) DEFAULT '0' COMMENT '0-不是高管 1-是高管',
  `position_tag` varchar(128) DEFAULT NULL COMMENT '职位',
  `identity_number_tag` varchar(20) DEFAULT NULL COMMENT '身份证号',
"""

eh_organizations = """
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT 'id of the record',
  `parent_id` bigint(20) DEFAULT NULL COMMENT 'id of the parent region',
  `organization_type` varchar(64) DEFAULT NULL COMMENT 'NONE, PM(Property Management), GARC(Resident Committee), GANC(Neighbor Committee), GAPS(Police Station)',
  `name` varchar(128) DEFAULT NULL,
  `address_id` bigint(20) NOT NULL DEFAULT '0' COMMENT 'address for department',
  `description` text,
  `path` varchar(128) DEFAULT NULL COMMENT 'path from the root',
  `level` int(11) NOT NULL DEFAULT '0',
  `status` tinyint(4) NOT NULL DEFAULT '1' COMMENT '1: inactive, 2: active, 3: locked, 4: mark as deleted',
  `department_type` varchar(64) DEFAULT NULL,
  `group_type` varchar(64) DEFAULT NULL COMMENT 'ENTERPRISE, DEPARTMENT, GROUP, JOB_POSITION, JOB_LEVEL, MANAGER',
  `create_time` datetime DEFAULT NULL,
  `update_time` datetime DEFAULT NULL,
  `directly_enterprise_id` bigint(20) NOT NULL DEFAULT '0' COMMENT 'directly under the company',
  `namespace_id` int(11) NOT NULL DEFAULT '0',
  `group_id` bigint(20) DEFAULT NULL COMMENT 'eh_group id',
  `integral_tag1` bigint(20) DEFAULT NULL,
  `integral_tag2` bigint(20) DEFAULT NULL,
  `integral_tag3` bigint(20) DEFAULT NULL,
  `integral_tag4` bigint(20) DEFAULT NULL,
  `integral_tag5` bigint(20) DEFAULT NULL,
  `string_tag1` varchar(128) DEFAULT NULL,
  `string_tag2` varchar(128) DEFAULT NULL,
  `string_tag3` varchar(128) DEFAULT NULL,
  `string_tag4` varchar(128) DEFAULT NULL,
  `string_tag5` varchar(128) DEFAULT NULL,
  `show_flag` tinyint(4) DEFAULT '1',
  `namespace_organization_token` varchar(256) DEFAULT NULL COMMENT 'the token from third party',
  `namespace_organization_type` varchar(128) DEFAULT NULL COMMENT 'the type of organization',
  `size` int(11) DEFAULT NULL COMMENT 'job level size',
"""

import re

def transfer(table):
    lines = table.splitlines()

    for line in lines:
        if not line:
            continue
        res = line
        res = re.sub(r'(.*) COMMENT.*$', r'\1', res)
        if res.find('varchar') == -1:
            res = re.sub(r'(.*)\(\d*\)(.*)', r'\1\2', res)
        res = res.replace('  `', '', 1)\
        .replace('`', ' = Column(', 1)\
        .replace(' bigint ', ' BIGINT, ', 1)\
        .replace(' int ', ' INTEGER, ', 1)\
        .replace(' tinyint ', ' TINYINT, ', 1)\
        .replace(' datetime ', ' DATETIME, ', 1)\
        .replace(' text', ' TEXT,', 1)\
        .replace('varchar', 'VARCHAR', 1)\
        .replace(' NOT NULL ', ' nullable=False, ', 1)\
        .replace(' AUTO_INCREMENT', ' autoincrement=True', 1)\
        .replace(' DEFAULT ', ' default=', 1)\
        .replace('NULL', "'NULL'", 1)\
        .rstrip(',')\
        .replace(')', '),', 1)

        res = res + ' )'
        print(res)

tables = [
    # eh_banners,
    # eh_launch_pad_items,
    # eh_launch_pad_layouts
    # eh_namespaces
    # eh_namespace_details
    # eh_item_service_categries
    eh_communities,
    eh_regions,
    eh_users,
    eh_organizations
]

if __name__ == '__main__':
    for table in tables:
        transfer(table)
        print("\n\n")
