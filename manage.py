#!/usr/bin/env python
"""
manage脚本，用来启动flask服务器，以及一些其它辅助功能

默认情况下，runserver在本地特定端口 启动dev环境服务器，而后其端口就可以访问了

.. code-block:: bash

   ./manage.py runserver -h 0.0.0.0 -p 5000

在浏览器访问 http://localhost:5000，出现 Hello, Here，说明服务器启动成功

如果要在生产环境下启动服务器，需要声明环境变量

.. code-block:: bash

   FLASK_ENV=production ./manage.py runserver -h 0.0.0.0 -p 5000

manage.py的其它功能

.. code-block:: bash

   usage: manage.py [-?] {test,shell,db,runserver} ...

   positional arguments:
       runserver           启动flask服务器
       shell               启动ipython辅助shell，帮助调试变量，数据库连接之类，非常有用的命令
       test                单元测试，不完善，可暂时不需要
       db                  针对ORM的修改，进行数据库表的迁移修改，因为数据库是固定的，所以这里暂时不需要

   optional arguments:
     -?, --help            show this help message and exit

"""
import os
from app import create_app, db
import app.model as models
from flask_script import Manager, Shell
from flask_migrate import MigrateCommand

app = create_app(os.getenv('FLASK_ENV') or 'default')
manager = Manager(app)


def make_shell_context():
    return dict(app=app, db=db, models=models)


manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def test():
    import pytest
    pytest.main(['-n', 4, '-vs', '.'])

if __name__ == '__main__':
    manager.run()