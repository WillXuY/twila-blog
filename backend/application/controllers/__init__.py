"""
Controller layer: handles incoming HTTP requests.

Each controller module defines route handlers (Flask Blueprints) that:
- Parse request arguments
- Call corresponding services
- Return standardized JSON responses
"""

from .main_controller import main_bp
from .chat_controller import chat_bp

__all__ = ['main_bp', 'chat_bp']
