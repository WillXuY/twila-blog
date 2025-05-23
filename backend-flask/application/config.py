import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "postgresql://twila_app:pw.@pgsql:5432/twila_blog")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get("SECRET_KEY", "fallback-secret")

    # 新增 Ollama 配置
    OLLAMA_ENDPOINTS = [
        # {
        #     "url": "http://host.containers.internal:11435/api/chat",
        #     "model": "deepseek-r1:8b"
        # },
        {
            "url": "http://ollama:11434/api/chat",
            "model": "qwen2.5:0.5b"
        }
    ]
