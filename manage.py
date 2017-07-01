#!/usr/bin/env python
"""
manage script do many things for us

we may start dev server many times during development.

.. code-block:: bash

   ./manage.py runserver -h 0.0.0.0 -p 5000

browse http://localhost:5000 and see if it works

you need FLASK_ENV to change the current environment like production or other.

.. code-block:: bash

   FLASK_ENV=production ./manage.py runserver -h 0.0.0.0 -p 5000

detail about manage.py usage

.. code-block:: bash

   usage: manage.py [-?] {test,shell,db,runserver} ...

   positional arguments:
       runserver           start flask server
       shell               run ipython shell for debug
       test                run unit tests
       db                  db magrition

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
