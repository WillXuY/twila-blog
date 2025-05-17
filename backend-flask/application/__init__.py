from flask import Flask
from .models import db
from application.routes import main_bp, chat_bp, conversations_bp, messages_bp
from application.config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # 初始化模型和 migrate 实现 alembic 自动管理数据库
    db.init_app(app)

    # 注册蓝图
    app.register_blueprint(main_bp)             # 根路由（主页）
    app.register_blueprint(chat_bp, url_prefix='/chat')  # 聊天功能路由
    # 查询聊天历史的功能
    app.register_blueprint(conversations_bp, url_prefix='/chat/conversations')
    app.register_blueprint(messages_bp, url_prefix='/chat/conversations')

    return app
