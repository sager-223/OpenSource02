from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pymysql
from config import config_map
pymysql.install_as_MySQLdb()

db = SQLAlchemy()
def create_app(config_name='develop'):
    # 初始化app对象
    app = Flask(__name__)
    config = config_map[config_name]
    app.config.from_object(config)

    # 加载数据库
    db.init_app(app)

    # 注册蓝图
    from . import api_1_0
    app.register_blueprint(api_1_0.api,url_prefix="/show")

    return app