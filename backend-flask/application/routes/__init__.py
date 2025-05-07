from .main import main_bp  # 只导入蓝图
from .chat import chat_bp
from .conversations import conversations_bp
from .messages import messages_bp

__all__ = ['main_bp', 'chat_bp', 'conversations_bp', 'message_bp']
