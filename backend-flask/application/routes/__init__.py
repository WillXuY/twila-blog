from .main import main_bp  # 只导入蓝图
from .chat import chat_bp

__all__ = ['main_bp', 'chat_bp']  # 可选，控制从该模块 import * 时暴露的接口
