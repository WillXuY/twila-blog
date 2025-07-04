from typing import Dict, Iterable
from config.base import BaseConfig


def from_config(config: BaseConfig, keys: Iterable[str] = None) -> Dict[str, str]:
    env = config.env_dict
    default_keys = [
        "POSTGRESQL_USER",
        "POSTGRESQL_PASSWORD",
        "POSTGRESQL_DB",
        "PG_CONTAINER_NAME",
        "PG_IMAGE",
        "PGDATA_DIR",
        "NETWORK_ARG",
    ]
    keys = keys or default_keys
    return {key: env.get(key, "") for key in keys}
