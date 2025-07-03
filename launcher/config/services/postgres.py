from typing import Dict
from config.base import BaseConfig


def from_config(config: BaseConfig) -> Dict[str, str]:
    env = config.env_dict
    return {
        "POSTGRES_USER": env["POSTGRESQL_USER"],
        "POSTGRES_PASSWORD": env["POSTGRESQL_PASSWORD"],
        "POSTGRES_DB": env["POSTGRESQL_DB"],
        "PG_CONTAINER_NAME": env["PG_CONTAINER_NAME"],
        "PG_IMAGE": env["PG_IMAGE"],
        "PGDATA_DIR": env["PGDATA_DIR"],
        "NETWORK_ARG": env["NETWORK_ARG"],
    }
