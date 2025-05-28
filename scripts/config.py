import os
import json
import subprocess

BASE_SECRET_PATH = "../secrets"
DEFAULT_ENV = "prod"

PG_CONTAINER_NAME = "pgsql"
PG_IMAGE = "quay.io/willxuy/postgres:latest"
PGDATA_DIR = os.path.expanduser("~/.local/share/containers/postgres/data")

NETWORK_NAME = "twila-network"
NETWORK_ARG = {
    "dev": "-p 127.0.0.1:11434:11434",
    "prod": f"--network {NETWORK_NAME}"
}

OLLAMA_CONFIG = {
    "dev": [
        {"url": "http://localhost:11434/api/chat", "model": "deepseek-coder:6.7b"},
        {"url": "http://localhost:11434/api/chat", "model": "qwen2.5:0.5b"},
    ],
    "prod": [
        {"url": "http://ollama:11434/api/chat", "model": "qwen2.5:0.5b"},
    ],
}


def get_ollama_config(env: str = DEFAULT_ENV) -> dict:
    """
    获取 Ollama 配置
    """
    network_config = NETWORK_ARG.get(env, NETWORK_ARG[DEFAULT_ENV])

    return {
        "NETWORK_ARG": network_config
    }


def decrypt_env_file(env: str = DEFAULT_ENV) -> dict:
    """
    读取加密的 ../secrets/.env.{env}.gpg 文件，使用 gpg 解密后，返回环境变量字典。
    """
    env_file_path = os.path.join(BASE_SECRET_PATH, f".env.{env}.gpg")
    if not os.path.exists(env_file_path):
        raise FileNotFoundError(f"环境配置文件不存在: {env_file_path}")

    # 使用 gpg 解密，要求本地已经有对应密钥
    try:
        result = subprocess.run(
            ["gpg", "--decrypt", env_file_path],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"解密环境文件失败: {e.stderr.strip()}") from e

    env_vars = {}
    for line in result.stdout.splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, val = line.split("=", 1)
        env_vars[key.strip()] = val.strip().strip('"').strip("'")

    return env_vars


def get_postgres_config(env: str = DEFAULT_ENV) -> dict:
    """
    读取指定环境的 PostgreSQL 配置，严格使用 POSTGRESQL_USER、POSTGRESQL_PASSWORD、POSTGRESQL_DB。
    """
    env_vars = decrypt_env_file(env)

    postgres_user = env_vars.get("POSTGRESQL_USER")
    postgres_password = env_vars.get("POSTGRESQL_PASSWORD")
    postgres_db = env_vars.get("POSTGRESQL_DB")

    if not all([postgres_user, postgres_password, postgres_db]):
        raise ValueError(
            "PostgreSQL 环境变量不完整，缺少 POSTGRESQL_USER、POSTGRESQL_PASSWORD 或 POSTGRESQL_DB"
        )

    network_arg = "" if env == "dev" else f"--network {NETWORK_NAME}"

    return {
        "POSTGRES_USER": postgres_user,
        "POSTGRES_PASSWORD": postgres_password,
        "POSTGRES_DB": postgres_db,
        "PG_CONTAINER_NAME": PG_CONTAINER_NAME,
        "PG_IMAGE": PG_IMAGE,
        "PGDATA_DIR": PGDATA_DIR,
        "NETWORK_ARG": network_arg
    }


def get_flask_config(env: str = DEFAULT_ENV) -> dict:
    env_vars = decrypt_env_file(env)

    database_url = env_vars.get("DATABASE_URL")
    secret_key = env_vars.get("SECRET_KEY")

    if not database_url or not secret_key:
        raise ValueError("缺少必要的 Flask 配置：DATABASE_URL 或 SECRET_KEY")

    flask_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend-flask"))

    # 把当前环境的 OLLAMA_CONFIG 转成 JSON 字符串
    ollama_json = json.dumps(OLLAMA_CONFIG.get(env, OLLAMA_CONFIG[DEFAULT_ENV]))

    # 读取版本
    version_file = os.path.join(flask_root, "VERSION")
    with open(version_file, "r") as f:
        version = f.read().strip()

    return {
        "DATABASE_URL": database_url,
        "SECRET_KEY": secret_key,
        "PYTHONPATH": flask_root,
        "OLLAMA_ENDPOINTS": ollama_json,
        "VERSION": version
    }
