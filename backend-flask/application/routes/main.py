import uuid
from flask import Blueprint, render_template, request

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    # 每次都生成一个新的 UUID，前端按需使用
    server_generated_user_id = str(uuid.uuid4())
    return render_template('chat_ai.html', server_user_id=server_generated_user_id)
