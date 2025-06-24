import json

from dotenv import dotenv_values
from pathlib import Path
from typing import Dict

# 固定配置部分
COMMAND_REQUIRED = {"podman": "--version"}

# 动态定位项目根目录的 env.example 文件路径
PROJECT_ROOT = Path(__file__).parents[2]
ENV_FILE = PROJECT_ROOT / "env.example"
# 只读取，不修改 os.environ
_config = dotenv_values(dotenv_path=ENV_FILE)


def _get_config(key: str, default: str) -> str:
    value = _config.get(key, default)
    return value if isinstance(value, str) else default


PG_CONTAINER_NAME = "pgsql"
PG_IMAGE = "quay.io/willxuy/postgres:latest"
PGDATA_DIR = str(Path.home() / ".local/share/containers/postgres/data")
# dev 环境不需要额外配置网络
PG_NETWORK_ARG = ""

OLLAMA_NETWORK_ARG = "-p 127.0.0.1:11434:11434"

FLASK_APP_ENV = "dev"
FLASK_MODEL_CONFIG = json.dumps([
    {"url": "http://localhost:11434/api/chat", "model": "deepseek-coder:6.7b"},
    {"url": "http://localhost:11434/api/chat", "model": "qwen2.5:0.5b"},
])


def get_postgres_config() -> Dict[str, str]:
    return {
        "POSTGRES_USER": _get_config("POSTGRESQL_USER", "postgres"),
        "POSTGRES_PASSWORD": _get_config("POSTGRESQL_PASSWORD", "dev.secret"),
        "POSTGRES_DB": _get_config("POSTGRESQL_DB", "postgres"),
        "PG_CONTAINER_NAME": PG_CONTAINER_NAME,
        "PG_IMAGE": PG_IMAGE,
        "PGDATA_DIR": PGDATA_DIR,
        "NETWORK_ARG": PG_NETWORK_ARG,
    }


def get_ollama_config() -> Dict[str, str]:
    return {
         "NETWORK_ARG": OLLAMA_NETWORK_ARG
    }


def get_flask_config() -> Dict[str, str]:
    return {
        "DATABASE_URL": _get_config("DATABASE_URL", "flask.database.url"),
        "SECRET_KEY": _get_config("SECRET_KEY", "flask.key"),
        "OLLAMA_ENDPOINTS": FLASK_MODEL_CONFIG,
        "APP_ENV": FLASK_APP_ENV
    }
