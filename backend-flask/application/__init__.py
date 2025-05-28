"""
Application package initializer.
"""

from flask import Flask

from .config import Config
from .controllers import main_bp, chat_bp
from .errors.error_handlers import register_error_handlers
from .extensions import db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # 数据库初始化
    db.init_app(app)

    # 注册蓝图
    app.register_blueprint(main_bp)
    app.register_blueprint(chat_bp, url_prefix='/chat')

    # 全局错误处理
    register_error_handlers(app)

    return app
