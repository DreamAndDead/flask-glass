from flask import url_for
from flask import json


def api_data(client, path, param):
    return client.post(
        url_for('main.' + path),
        data=json.dumps(param),
        content_type='application/json'
    ).json


class TestApis:
    def test_load(self, client):
        # 使用深业物业的测试数据，提前进行数据库表数据的修改，检测约定结果
        param = dict(
            ns=999984,
            scene='pm_admin',
            layout='ServiceMarketLayout',
            scope_id=0,
            scope_code=0
        )
        result = api_data(client, 'load', param)
        assert 'displayName' in result
        assert 'groups' in result

    def test_save(self, client):
        selector = dict(
            ns=999984,
            scene='pm_admin',
            layout='ServiceMarketLayout',
            scope_id=0,
            scope_code=0
        )
        data = api_data(client, 'load', selector)
        param = dict(
            selector=selector,
            data=data
        )
        assert api_data(client, 'save', param) == dict(status='success')

    def test_get_category_list(self, client):
        data = api_data(client, 'get_category_list', dict(ns=999984, scene='default'))
        assert 'categorylist' in data

        list = data.get('categorylist')
        length = len(list)
        assert length > 0
        item = list[0]
        assert 'id' in item
        assert 'name' in item

        api_data(client, 'add_category', dict(ns=999984, name='zdw', scene='default'))
        data = api_data(client, 'get_category_list', dict(ns=999984, scene='default'))
        new_length = len(data.get('categorylist'))
        assert new_length == length + 1

        api_data(client, 'del_category', dict(ns=999984, id=15, scene='default'))
        data = api_data(client, 'get_category_list', dict(ns=999984, scene='default'))
        del_length = len(data.get('categorylist'))
        assert del_length == new_length - 1

    def test_get_used_scope_list(self, client):
        data = api_data(client, 'get_used_scope_list', dict(ns=0, scene='pm_admin'))
        assert 'scopelist' in data
        list = data.get('scopelist')
        assert len(list) > 0
        pickone = list[0]
        assert 'name' in pickone
        assert 'id' in pickone
        assert 'code' in pickone

    def test_get_scope_name(self, client):
        data = api_data(client, 'get_scope_name', dict(ns=0, code=3, id=4))
        assert 'name' in data
        assert data.get('name') == 'locke'
        data = api_data(client, 'get_scope_name', dict(ns=0, code=2, id=10002))
        assert data.get('name') == '北京市'

    def test_del_scope(self, client):
        api_data(client, 'del_scope', dict(ns=1000000, scene='park_tourist', scope_code=0, scope_id=0))
        data = api_data(client, 'get_used_scope_list', dict(ns=1000000, scene='park_tourist'))
        assert len(data.get('scopelist')) == 0

    def test_get_used_layout_list(self, client):
        data = api_data(client, 'get_used_layout_list', dict(ns=1000000, scene='pm_admin', scope_code=0, scope_id=0))
        assert 'layoutlist' in data
        assert len(data.get('layoutlist')) == 0

    def test_del_layout(self, client):
        api_data(client, 'del_layout', dict(ns=1000000, scene='pm_admin', scope_code=0, scope_id=0, layout_name='ServiceMarketLayout'))
        data = api_data(client, 'get_used_layout_list', dict(ns=1000000, scene='pm_admin', scope_code=0, scope_id=0))
        assert 'layoutlist' in data
        assert len(data.get('layoutlist')) == 0

