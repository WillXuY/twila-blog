"""
Application package initializer.
"""
import os

from flask import Flask
from flask_smorest import Api

from .config import CONFIG_MAP
from .config.base import APP_ENV
from .controllers import main_bp, chat_bp
from .errors.error_handlers import register_error_handlers
from .extensions import db


def init_api(app) -> None:
    app.config["API_TITLE"] = "Twila Blog API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_URL_PREFIX"] = "/api"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://unpkg.com/swagger-ui-dist/"


def create_app() -> Flask:
    app = Flask(__name__)

    app_env = os.environ.get("APP_ENV", APP_ENV.DEVELOPMENT.value)
    app.config.from_object(CONFIG_MAP.get(app_env))

    # 数据库初始化
    db.init_app(app)

    if APP_ENV.PRODUCTION.value == app_env:
        app.register_blueprint(chat_bp, url_prefix='/chat')
    else:
        init_api(app)
        api = Api(app, spec_kwargs={"servers": [{"url": "/api"}]})
        api.register_blueprint(chat_bp, url_prefix='/chat')

    # 注册普通蓝图
    app.register_blueprint(main_bp)

    # 全局错误处理
    register_error_handlers(app)

    return app
