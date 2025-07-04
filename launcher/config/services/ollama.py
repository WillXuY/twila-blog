from typing import Dict, Iterable
from config.base import BaseConfig


def from_config(config: BaseConfig, keys: Iterable[str] = None) -> Dict[str, str]:
    env = config.env_dict
    default_keys = [
        "NETWORK_ARG",
    ]
    keys = keys or default_keys
    return {key: env.get(key, "") for key in keys}
