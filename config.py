"""
在开发应用时，我们需要 test, development, production 三种不同的环境，对应不同的全局变量配置，比如连接哪个数据库，是否启动flask
的DEBUG选项，是否打印versose日志等

默认情况下，runserver在dev环境下启动，如果要切换环境，需要显式声明环境变量 FLASK_ENV=production or FLASK_ENV=test

此模块设置了所有环境下，Server的启动配置
"""
import os


class BaseConfig:
    """
    所有配置所共享的相同配置

    1. SECRET_KEY
    2. 服务器的ip与端口
    3. 静态资源的上传目录地址
    """
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess'
    HOST = '0.0.0.0'
    PORT = 5000
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'files')
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(BaseConfig):
    """
    Development开发环境下的配置，主要设置了

    1. 连接本地的数据库
    2. 启用flask DEBUG选项
    3. 加印操作数据库的日志消息
    """
    DEBUG = True
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = "mysql://root:root@localhost/development"


class TestConfig(BaseConfig):
    """
    Test测试环境下的配置，主要设置了

    1. 连接本地的测试数据库
    2. 启用flask DEBUG和TESTING选项
    3. 加印操作数据库的日志消息
    """
    DEBUG = True
    TESTING = True
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = "mysql://root:root@localhost/testdb"


class ProductionConfig(BaseConfig):
    """
    Production生产环境下的配置，主要设置了

    1. 连接服务器的数据库
    2. 去除了 开发，测试 环境下的辅助选项
    """
    SQLALCHEMY_DATABASE_URI = "mysql://<address online>"


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'test': TestConfig,

    'default': DevelopmentConfig
}
