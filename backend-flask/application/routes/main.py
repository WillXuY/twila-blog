from flask import Blueprint, render_template, request
import uuid

main_bp = Blueprint('main', __name__)

# 首页：index.html
@main_bp.route('/')
def home():
    return render_template('index.html')

# Chat 页面：chat_ai.html
@main_bp.route('/chat')
def chat():
    server_generated_user_id = str(uuid.uuid4())
    return render_template('chat_ai.html', server_user_id=server_generated_user_id)
