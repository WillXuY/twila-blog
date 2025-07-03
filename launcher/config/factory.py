"""
配置工厂模块。

功能：
- 根据环境名（"dev" 或 "prod"）加载对应的配置文件
- 如果配置不存在，触发交互式提示，生成 GPG 加密配置和 SQL 初始化脚本
- 解密 `.env.gpg` 文件，得到配置字典
- 提取并构造每个服务（Flask, PostgreSQL, Ollama）的配置对象

公开接口：
- get_config(env: Literal["dev", "prod"]) -> dict[str, Any]
"""

from config.base import BaseConfig, DevConfig, ProdConfig
from config.services.postgres import from_config as pg_config_from
from config.services.flask import from_config as flask_config_from
from config.services.ollama import from_config as ollama_config_from

from pathlib import Path
import subprocess
import questionary
import secrets
import logging
import string

logger = logging.getLogger(__name__)


def generate_env_and_sql(env: str, env_path: Path, sql_path: Path, pg_container_name: str) -> None:
    """
    当配置文件不存在时，交互式引导用户生成 .env.gpg 和 init SQL 文件。
    """
    env_path.parent.mkdir(parents=True, exist_ok=True)
    print(f"未检测到 {env} 环境的配置文件，将引导您生成")

    # 显示已有 GPG 密钥供选择
    subprocess.run(["gpg", "--list-keys"])

    gpg_recipient = questionary.text("请输入加密用的 GPG 接收者 ID 或邮箱：").ask()
    postgres_password = questionary.password("请设置 PostgreSQL 超级管理员 postgres 的密码：").ask()
    db_admin_password = questionary.password("请设置项目数据库管理员 twila_admin 的密码：").ask()
    db_app_password = questionary.password("请设置后台访问用户 twila_app 的密码：").ask()
    secret_key = "".join(secrets.choice(string.ascii_letters + string.digits) for _ in range(64))

    env_content = f"""\
POSTGRESQL_USER=postgres
POSTGRESQL_PASSWORD={postgres_password}
POSTGRESQL_DB=postgres
DATABASE_URL=postgresql://twila_app:{db_app_password}@{pg_container_name}:5432/twila_blog
SECRET_KEY={secret_key}
"""
    # 渲染 init SQL
    from jinja2 import Template
    from config.base import BaseConfig

    template_path = BaseConfig.INIT_DATABASE_SQL_TEMPLATE_PATH
    with template_path.open(encoding="utf-8") as f:
        tpl = Template(f.read())

    rendered = tpl.render(dba_password=db_admin_password, app_password=db_app_password)
    sql_path.write_text(rendered, encoding="utf-8")
    logger.info(f"初始化 SQL 已写入: {sql_path}")

    try:
        subprocess.run(
            ["gpg", "--yes", "--output", str(env_path), "--encrypt", "-r", gpg_recipient],
            input=env_content,
            text=True,
            check=True,
        )
        logger.info(f"{env} 配置已加密并保存为 {env_path}")
    except subprocess.CalledProcessError as e:
        logger.error("❌ GPG 加密失败！" + e.output)
        if env_path.exists():
            env_path.unlink()
        if sql_path.exists():
            sql_path.unlink()
        raise SystemExit(1)


def get_config(env: str) -> BaseConfig:
    """
    工厂方法，根据环境初始化配置对象。
    如果配置不存在，先执行交互式生成。
    返回 DevConfig / ProdConfig 的实例。
    """
    if env == "dev":
        path = DevConfig.ENV_DEV_GPG_PATH
        sql = DevConfig.DEV_INIT_DATABASE_SQL_PATH
        cls = DevConfig
    elif env == "prod":
        path = ProdConfig.ENV_PROD_GPG_PATH
        sql = ProdConfig.PROD_INIT_DATABASE_SQL_PATH
        cls = ProdConfig
    else:
        raise ValueError(f"不支持的环境类型: {env}")

    if not path.exists():
        generate_env_and_sql(env, path, sql, pg_container_name=BaseConfig.PG_CONTAINER_NAME)

    return cls()


def get_service_configs(env: str) -> dict:
    """
    高阶工厂：返回按服务分类的配置字典（pg, flask, ollama）。
    """
    config = get_config(env)
    env_dict = config.env_dict

    return {
        "pg": pg_config_from(env_dict),
        "flask": flask_config_from(env_dict),
        "ollama": ollama_config_from(env_dict),
    }
