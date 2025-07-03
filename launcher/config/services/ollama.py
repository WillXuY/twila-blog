from typing import Dict
from config.base import BaseConfig


def from_config(config: BaseConfig) -> Dict[str, str]:
    env = config.env_dict
    return {
        "NETWORK_ARG": env["NETWORK_ARG"],
    }
