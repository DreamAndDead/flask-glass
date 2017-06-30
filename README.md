# flask-glass
simple boilerplate for starting a new flask project. inspired by book [Flask Web
Development][book]

![cover][book cover]

features:
- db migration
- manage.py script
- unit test
- code doc generation

## pre

prepare virtualenv

    sudo pip install -U virtualenv

clone code

    git clone https://github.com/DreamAndDead/flask-glass.git

init virtualenv

    cd flask-glass

    virtualenv -p python3 .venv

    source .venv/bin/activate

install deps

    pip install -r requirements.txt

## about environment

we make every operation using script `./manage.py` later. here is one important
concept: environment.

- development environment
- test environment
- production environment

every environment gets its own configuration. check file `./config.py`.
modify the configuration according to your needs.

```python
class DevelopmentConfig(BaseConfig):
    DEBUG = True
    # ...

class TestConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    # ...

class ProductionConfig(BaseConfig):
    # ...
```

global env variable FLASK_ENV figure out which environment we are in.

    # development (default)
    ./manage.py ...
    FLASK_ENV=development ./manage.py ...
    # test
    FLASK_ENV=test ./manage.py ...
    # production
    FLASK_ENV=production ./manage.py ...

remember where you are.

## db migration

ensure mysqld is running, start it if you need

    service mysqld status

ensure database address is correct, see file `./config.py`

```python
# change the three SQLALCHEMY_DATABASE_URI s base on your machine
SQLALCHEMY_DATABASE_URI = "mysql://root:root@localhost/development"
SQLALCHEMY_DATABASE_URI = "mysql://root:root@localhost/testdb"
SQLALCHEMY_DATABASE_URI = "mysql://<address online>"
```

ensure database exist on your connected mysql, create it if you need

    mysql -u root -p
    create database development (or other)

migration init once

    ./manage.py db init

migrate db, build tables in database base on your *.py in  `./model`. every time
you modify the model files, remember run the commands again.

    ./manage.py db upgrade
    ./manage.py db migrate

refs:
- flask-migrate, thanks [visit doc][flask migrate]
- flask-SQLAlchemy, same api for many different databases. [visit doc][flask
    SQLAlchemy]

## start server

ensure you have made the migration and all db connections work

    ./manage.py runserver

browse `localhost:5000` to see

refs:
- flask-script make starting server and other things easily. [visit doc][flask script]
- flask-cors, cross domain. [visit doc][flask cors]

## test

run test

    ./manage.py test

all the test is in `./tests` folder.

refs:
- pytest as test runner. [visit doc][pytest]
- pytest-flask provide fixtures. [visit doc][pytest flask]
- pytest-xdist helps running tests in parallel. [visit doc][pytest xdist]

## docs

live doc

    make live

it'll automatically open the doc link in browser.

refs:
- sphinx and its plugins. [visit doc][sphinx]
- sphinx-autobuild make doc live. [visit doc][sphinx autobuild]

## shell

trust me, it's the most helpful command to help you debug your app.

    ./manage.py shell

`app`, `db` and `models` are avialable in this shell.

## END
[flask migrate]: https://flask-migrate.readthedocs.io/en/latest/
[flask script]: https://flask-script.readthedocs.io/en/latest/
[flask SQLAlchemy]: http://flask-sqlalchemy.pocoo.org/2.1/
[flask cors]: https://flask-cors.readthedocs.io/en/latest/

[pytest]: https://doc.pytest.org/
[pytest flask]: http://pytest-flask.readthedocs.io/en/latest/
[pytest xdist]: https://pypi.python.org/pypi/pytest-xdist

[sphinx]: http://www.sphinx-doc.org/en/stable/
[sphinx autobuild]: https://pypi.python.org/pypi/sphinx-autobuild

[book]: http://shop.oreilly.com/product/0636920031116.do
[book cover]: https://covers.oreillystatic.com/images/0636920031116/lrg.jpg
