import json
import questionary
import subprocess

from pathlib import Path
from typing import Dict

# 固定配置部分
COMMAND_REQUIRED = {"podman": "--version", "gpg": "--list-keys"}

# 动态定位项目根目录的 env.example 文件路径
PROJECT_ROOT = Path(__file__).parents[2]
ENV_EXAMPLE = PROJECT_ROOT / "env.example"
SECRETS_PATH = PROJECT_ROOT / "secrets"
ENV_PROD_GPG_FILE = SECRETS_PATH / ".env.prod.gpg"


def decrypt_env_file(file_path: str) -> dict[str, str]:
    """解密 .env.prod.gpg 文件并将内容解析为字典返回，不生成临时文件。"""
    result = subprocess.run(
        ["gpg", "--decrypt", file_path],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    decrypted_content = result.stdout
    env_dict = {}
    for line in decrypted_content.splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        env_dict[key.strip()] = value.strip()
    return env_dict


def prompt_user_for_env() -> dict[str, str]:
    print("未找到 secrets/.env.prod.gpg，开始交互式配置...")
    db_password = questionary.password("请输入数据库密码: ").ask()
    # 其他必填环境变量输入
    # 生成 .env.prod 文件并加密保存为 .env.prod.gpg
    print("保存加密后的环境变量文件")


def prepare_prod_env() -> dict[str, str]:
    if ENV_PROD_GPG_FILE.exists():
        env_dict = decrypt_env_file(str(ENV_PROD_GPG_FILE))
        return env_dict
    else:
        env_dict = prompt_user_for_env()
        return env_dict




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
