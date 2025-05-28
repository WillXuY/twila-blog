import os
import json


class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "postgresql://twila_app:pw.@localhost:5432/twila_blog")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get("SECRET_KEY", "fallback-secret")

    # 新增：从环境变量读取 OLLAMA_ENDPOINTS（字符串），并尝试解析为 JSON
    _ollama_raw = os.environ.get("OLLAMA_ENDPOINTS", "[]")
    try:
        OLLAMA_ENDPOINTS = json.loads(_ollama_raw)
    except json.JSONDecodeError:
        OLLAMA_ENDPOINTS = []
