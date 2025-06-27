import os
import json

from .base import BaseConfig

DEFAULT_DATABASE_URL = "postgresql://twila_app:pw.@localhost:5432/twila_blog"
DEFAULT_SECRET_KEY = ""

DEFAULT_OLLAMA_CONFIG = [{"url": "http://localhost:11434/api/chat", "model": "qwen2.5:0.5b"}]


class DevConfig(BaseConfig):
    DEBUG = True
    FLASK_RUN_HOST = "127.0.0.1"
    FLASK_RUN_PORT = 5000

    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", DEFAULT_DATABASE_URL)
    SECRET_KEY = os.environ.get("SECRET_KEY", DEFAULT_SECRET_KEY)

    _ollama_raw = os.environ.get("OLLAMA_ENDPOINTS")
    try:
        OLLAMA_ENDPOINTS = json.loads(_ollama_raw) if _ollama_raw else DEFAULT_OLLAMA_CONFIG
    except json.JSONDecodeError:
        print("解析 OLLAMA_ENDPOINTS 异常, 使用默认配置")
        OLLAMA_ENDPOINTS = DEFAULT_OLLAMA_CONFIG
