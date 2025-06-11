import os
import json

from typing import Dict

# 只支持 dev 环境
ENV = os.getenv("ENV", "dev")

# PostgreSQL 配置，来自环境变量或默认值
POSTGRES_USER = os.getenv("POSTGRESQL_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRESQL_PASSWORD", "dev.secret")
POSTGRES_DB = os.getenv("POSTGRESQL_DB", "postgres")
PG_CONTAINER_NAME = "pgsql"
PG_IMAGE = "quay.io/willxuy/postgres:latest"
PGDATA_DIR = os.path.expanduser("~/.local/share/containers/postgres/data")

# 网络参数
NETWORK_ARG = os.getenv("NETWORK_ARG", "-p 127.0.0.1:11434:11434")

# Flask 配置
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://twila_app:pw.@localhost:5432/twila_blog")
SECRET_KEY = os.getenv("SECRET_KEY", "default-secret-key-for-dev")

# Ollama 配置
OLLAMA_CONFIG = [
    {"url": "http://localhost:11434/api/chat", "model": "deepseek-coder:6.7b"},
    {"url": "http://localhost:11434/api/chat", "model": "qwen2.5:0.5b"},
]


def get_postgres_config() -> Dict[str, str]:
    return {
        "POSTGRES_USER": POSTGRES_USER,
        "POSTGRES_PASSWORD": POSTGRES_PASSWORD,
        "POSTGRES_DB": POSTGRES_DB,
        "PG_CONTAINER_NAME": PG_CONTAINER_NAME,
        "PG_IMAGE": PG_IMAGE,
        "PGDATA_DIR": PGDATA_DIR,
        "NETWORK_ARG": NETWORK_ARG,
    }


def get_flask_config() -> Dict[str, str]:
    flask_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend-flask"))
    ollama_json = json.dumps(OLLAMA_CONFIG)
    version_file = os.path.join(flask_root, "VERSION")
    try:
        with open(version_file, "r") as f:
            version = f.read().strip()
    except FileNotFoundError:
        version = "dev"

    return {
        "DATABASE_URL": DATABASE_URL,
        "SECRET_KEY": SECRET_KEY,
        "PYTHONPATH": flask_root,
        "OLLAMA_ENDPOINTS": ollama_json,
        "VERSION": version,
        "APP_ENV": "dev"
    }
