import uuid

from flask import Blueprint, render_template, current_app

from application.services.main_service import start_ollama_preheat

main_bp = Blueprint('main', __name__)

# 首页：index.html
@main_bp.route('/')
def home():
    # current_app 是一个代理，需要在请求上下文里使用
    app = current_app._get_current_object()
    # 用线程启动预热，不阻塞当前请求
    start_ollama_preheat(app)
    return render_template('index.html')

# Chat 页面：chat_ai.html
@main_bp.route('/chat')
def chat():
    server_generated_user_id = str(uuid.uuid4())
    return render_template('chat_ai.html', server_user_id=server_generated_user_id)
