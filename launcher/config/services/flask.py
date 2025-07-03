from typing import Dict
from config.base import BaseConfig


def from_config(config: BaseConfig) -> Dict[str, str]:
    env = config.env_dict
    return {
        "DATABASE_URL": env["DATABASE_URL"],
        "SECRET_KEY": env["SECRET_KEY"],
        "NETWORK_ARG": env["NETWORK_ARG"],
        "APP_ENV": env["FLASK_APP_ENV"],
    }
