from typing import Dict, Iterable
from config.base import BaseConfig


def from_config(config: BaseConfig, keys: Iterable[str] = None) -> Dict[str, str]:
    env = config.env_dict
    default_keys = [
        "DATABASE_URL",
        "SECRET_KEY",
        "OLLAMA_ENDPOINTS",
        "NETWORK_ARG",
        "FLASK_APP_ENV",
    ]
    keys = keys or default_keys
    return {key: env.get(key, "") for key in keys}
