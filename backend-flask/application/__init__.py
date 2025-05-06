from flask import Flask
from application.routes import main_bp, chat_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object('application.config.Config')

    # 注册蓝图
    app.register_blueprint(main_bp)             # 根路由（主页）
    app.register_blueprint(chat_bp, url_prefix='/chat')  # 聊天功能路由

    return app
