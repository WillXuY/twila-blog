"""
基础配置模块。

功能：
- 提供 BaseConfig 类：读取 GPG 加密的配置文件
- 实现通用功能：env 解密、交互式生成、secret key 生成、SQL 模板渲染
- 提供 DevConfig 和 ProdConfig，分别指定配置路径等环境特定参数

用法：
    config = DevConfig()
    env_dict = config.env_dict
"""
import subprocess

from pathlib import Path
from typing import Iterable, Final


class BaseConfig:
    REQUIRED_BASE_CONSTANTS: Final = [
        "PG_CONTAINER_NAME",
        "PG_IMAGE",
        "PGDATA_DIR",
    ]
    REQUIRED_SUBCLASS_CONSTANTS: Final = [
        "NETWORK_ARG",
        "COMMAND_REQUIRED",
        "FLASK_APP_ENV",
    ]
    # 文件路径相关内容
    PROJECT_ROOT_PATH: Final = Path(__file__).parents[2]
    SECRETS_PATH: Final = PROJECT_ROOT_PATH / "secrets"
    BACKEND_VERSION_PATH: Final = PROJECT_ROOT_PATH / "backend" / "VERSION"
    LAUNCHER_TEMPLATES_PATH: Final = PROJECT_ROOT_PATH / "launcher" / "templates"
    INIT_DATABASE_SQL_TEMPLATE_PATH: Final = LAUNCHER_TEMPLATES_PATH / "init_database.sql.j2"

    PG_CONTAINER_NAME: Final = "postgres"
    PG_IMAGE: Final = "quay.io/willxuy/postgres:latest"
    PG_DATA_DIR: Final = str(Path.home() / ".local/share/containers/postgres/data")

    def __init__(self, env_gpg_path: Path) -> None:
        if not env_gpg_path.exists():
            raise FileNotFoundError(f"GPG 文件未找到: {env_gpg_path}")
        self.env_gpg_path = env_gpg_path
        self.env_dict = self._decrypt_env_file()
        required_constants = self.REQUIRED_BASE_CONSTANTS + self.REQUIRED_SUBCLASS_CONSTANTS
        self._inject_static_defaults(required_constants)

    def _decrypt_env_file(self) -> dict[str, str]:
        result = subprocess.run(
            ["gpg", "--decrypt", str(self.env_gpg_path)],
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

    def _inject_static_defaults(self, required_constants: Iterable[str]) -> None:
        """
        将定义在类中的所有必须常量字段注入 env_dict 中（包含 Base 和子类字段）。
        """
        for key in required_constants:
            if not hasattr(self, key):
                raise AttributeError(f"{self.__class__.__name__} 缺少必须字段: {key}")
            self.env_dict[key] = getattr(self, key)


class DevConfig(BaseConfig):
    # 内部使用的内容
    ENV_GPG_PATH: Final = BaseConfig.SECRETS_PATH / ".env.dev.gpg"
    INIT_DATABASE_SQL_PATH: Final = BaseConfig.SECRETS_PATH / "dev_init_database.sql"

    # 提供通用调用的内容
    NETWORK_ARG: Final = ""
    COMMAND_REQUIRED: Final = {"podman": "--version"}
    FLASK_APP_ENV: Final = "dev"

    def __init__(self) -> None:
        super().__init__(self.ENV_GPG_PATH)


class ProdConfig(BaseConfig):
    # 内部使用的内容
    ENV_GPG_PATH: Final = BaseConfig.SECRETS_PATH / ".env.prod.gpg"
    INIT_DATABASE_SQL_PATH: Final = BaseConfig.SECRETS_PATH / "prod_init_database.sql"
    # 独立部分
    POD_NETWORK_NAME: Final = "twila_network"

    # 提供通用调用的内容
    NETWORK_ARG: Final = f"--network {POD_NETWORK_NAME}"
    COMMAND_REQUIRED: Final = {"podman": "--version", "gpg": "--list-keys"}
    FLASK_APP_ENV: Final = "prod"

    def __init__(self) -> None:
        super().__init__(self.ENV_GPG_PATH)
