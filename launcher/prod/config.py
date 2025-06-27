import json
import logging
import questionary
import secrets
import string
import subprocess

from jinja2 import Template
from pathlib import Path
from typing import Dict

from start_manager.common.utils import show_gpg_keys

# 固定配置部分
PODMAN_NERWORK_NAME = "twila_network"
COMMAND_REQUIRED = {"podman": "--version", "gpg": "--list-keys"}
# 统一的网络配置
POD_NETWORK_ARG = f"--network {PODMAN_NERWORK_NAME}"

# 动态定位项目根目录的 env.example 文件路径
PROJECT_ROOT = Path(__file__).parents[2]
BACKEND_VERSION_FILE = PROJECT_ROOT / "backend-flask" / "VERSION"
SECRETS_PATH = PROJECT_ROOT / "secrets"
ENV_PROD_GPG_FILE = SECRETS_PATH / ".env.prod.gpg"
INIT_DATABASE_SQL = SECRETS_PATH / "init_database.sql"
SQL_FILE_PATH = PROJECT_ROOT / "scripts" / "postgresql"
INIT_DATABASE_TEMPLATE = SQL_FILE_PATH / "init_database.sql.j2"

PG_CONTAINER_NAME = "pgsql"
PG_IMAGE = "quay.io/willxuy/postgres:latest"
PGDATA_DIR = str(Path.home() / ".local/share/containers/postgres/data")

FLASK_APP_ENV = "prod"
# todo 增加模型可配置功能
FLASK_MODEL_CONFIG = json.dumps([
    {"url": "http://ollama:11434/api/chat", "model": "qwen2.5:0.5b"},
])

logger = logging.getLogger(__name__)


class ProdConfig:
    def __init__(self) -> None:
        self.env_gpg_file = ENV_PROD_GPG_FILE
        if not self.env_gpg_file.exists():
            self.prompt_user_for_env()
        self.env_dict = self._decrypt_env_file()

    def _generate_secret_key(self) -> str:
        alphabet = string.ascii_letters + string.digits
        return ''.join(secrets.choice(alphabet) for _ in range(64))

    def _render_jinja2_sql_template(self, dba_password: str, app_password: str) -> None:
        """使用 Jinja2 渲染 init_database.sqql.j2 模板"""
        with open(INIT_DATABASE_TEMPLATE, encoding="utf-8") as f:
            template = Template(f.read())
        rendered = template.render(
            dba_password=dba_password,
            app_password=app_password,
        )
        INIT_DATABASE_SQL.write_text(rendered, encoding="utf-8")

    def prompt_user_for_env(self) -> None:
        """当 secrets/.env.prod.gpg 不存在时提供交互式配置"""
        SECRETS_PATH.mkdir(parents=True, exist_ok=True)
        show_gpg_keys()
        gpg_recipient = questionary.text("请输入加密用的 GPG 接收者, ID 或 email: ").ask()
        postgres_password = questionary.password("请设置 PostgreSQL 超级管理员 postgres 的密码: ").ask()
        db_admin_password = questionary.password("请设置项目数据库 twila_blog 管理员 twila_admin 的密码: ").ask()
        db_app_password = questionary.password("请设置后台项目访问用户 twila_app 的密码: ").ask()
        env_data = {
            "POSTGRESQL_USER": "postgres",
            "POSTGRESQL_PASSWORD": postgres_password,
            "POSTGRESQL_DB": "postgres",
            "DATABASE_URL": f"postgresql://twila_app:{db_app_password}@{PG_CONTAINER_NAME}:5432/twila_blog",
            "SECRET_KEY": self._generate_secret_key(),
        }
        env_content = "\n".join(f"{k}={v}" for k, v in env_data.items()) + "\n"
        # 调用 gpg 加密，输入通过 stdin，输出到 .env.prod.gpg
        self._render_jinja2_sql_template(db_admin_password, db_app_password)
        logger.info("初始化 secrets/init_database.sql 生成成功!")
        try:
            subprocess.run(
                ["gpg", "--yes", "--output", str(self.env_gpg_file), "--encrypt", "-r", gpg_recipient],
                input=env_content,
                text=True,
                check=True,
            )
            logger.info("环境变量已加密并保存为 secrets/.env.prod.gpg")
        except subprocess.CalledProcessError as e:
            if self.env_gpg_file.exists():
                self.env_gpg_file.unlink()
            if INIT_DATABASE_SQL.exists():
                INIT_DATABASE_SQL.unlink()
            logger.error("❌ GPG 加密失败，请检查 GPG 配置和接收者是否存在。")
            logger.error(f"错误码: {e.returncode}")
            logger.error(f"命令: {e.cmd}")
            # 不打印 e.stderr 或 env_content！
            raise SystemExit(1)

    def _decrypt_env_file(self) -> dict[str, str]:
        """解密 .env.prod.gpg 文件并解析为字典"""
        result = subprocess.run(
            ["gpg", "--decrypt", str(self.env_gpg_file)],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        env_dict = {}
        for line in result.stdout.splitlines():
            if "=" in line and not line.startswith("#"):
                key, value = line.strip().split("=", 1)
                env_dict[key.strip()] = value.strip()
        return env_dict

    def _get_env(self, key: str) -> str:
        result = self.env_dict.get(key)
        if result is None:
            raise KeyError(f"必要的环境变量 {key} 不存在！")
        return result

    def get_postgres_config(self) -> Dict[str, str]:
        return {
            "POSTGRES_USER": self._get_env("POSTGRESQL_USER"),
            "POSTGRES_PASSWORD": self._get_env("POSTGRESQL_PASSWORD"),
            "POSTGRES_DB": self._get_env("POSTGRESQL_DB"),
            "PG_CONTAINER_NAME": PG_CONTAINER_NAME,
            "PG_IMAGE": PG_IMAGE,
            "PGDATA_DIR": PGDATA_DIR,
            "NETWORK_ARG": POD_NETWORK_ARG,
        }

    def get_ollama_config(self) -> Dict[str, str]:
        return {
             "NETWORK_ARG": POD_NETWORK_ARG
        }

    def get_flask_config(self) -> Dict[str, str]:
        return {
            "DATABASE_URL": self._get_env("DATABASE_URL"),
            "SECRET_KEY": self._get_env("SECRET_KEY"),
            "OLLAMA_ENDPOINTS": FLASK_MODEL_CONFIG,
            "NETWORK": PODMAN_NERWORK_NAME,
            "APP_ENV": FLASK_APP_ENV,
            "VERSION": self._get_backend_version()
        }

    def _get_backend_version(self) -> str:
        if not BACKEND_VERSION_FILE.exists():
            raise FileNotFoundError(f"找不到版本文件: {BACKEND_VERSION_FILE}")
        version = BACKEND_VERSION_FILE.read_text(encoding="utf-8").strip()
        if not version:
            raise ValueError(f"{BACKEND_VERSION_FILE} 文件为空")
        return version
