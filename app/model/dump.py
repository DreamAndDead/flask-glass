"""
从相应的数据库中，导出sql语句
"""
import os
import sys

# import from sql file
# mysql -u username -p databasename < path/example.sql


def dump(ns=0):
    """
    导出sql文件

    .. todo::

        也许你很奇怪，这里只有一个参数ns，并没有数据库地址，要导出的数据库之类的参数，
        理论上应该是那样的，但是目前并不完善，相应的其它参数暂时写固定在dump函数里，后续这个函数需要修改

    input:

    .. code-block:: javascript

       { "ns": 0 }

    output:

        null

    """
    host = '127.0.0.1'
    user = 'root'
    passwd = 'root'
    db = 'development'
    tables = (
        'eh_banners',
        'eh_launch_pad_items',
        'eh_launch_pad_layouts',
        'eh_item_service_categries',
    )
    options = '--no-create-db --no-create-info --complete-insert --skip-add-locks --compact --extended-insert=false --order-by-primary '

    for table in tables:
        cmd = "mysqldump %s -h %s -u %s -p%s -w'namespace_id'='%s' %s %s > files/%s.sql" % (
            options, host, user, passwd, ns, db, table, table
        )
        os.system(cmd)

if __name__ == '__main__':
    if len(sys.argv) == 1:
        sys.exit('error! please use     %s [namespace_id]' % sys.argv[0])

    ns = sys.argv[1]
    dump(ns)


"""
!mysqldump -h 10.1.10.192 -u ehcore -pehcore ehcore_20160615 eh_communities eh_regions eh_users eh_organizations eh_banners eh_launch_pad_items eh_launch_pad_layouts eh_namespace_details eh_namespaces eh_item_service_categries | mysql -h localhost -u root -proot development
!mysqldump -h 10.1.10.192 -u ehcore -pehcore ehcore_20160615 eh_communities eh_regions eh_users eh_organizations eh_banners eh_launch_pad_items eh_launch_pad_layouts eh_namespace_details eh_namespaces eh_item_service_categries | mysql -h localhost -u root -proot test

yy
:@"

copy and run it. migarite database
"""
