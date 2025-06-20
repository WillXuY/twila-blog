import os
import json

from .base import BaseConfig


class ProdConfig(BaseConfig):
    DEBUG = False

    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    SECRET_KEY = os.environ.get("SECRET_KEY")

    def __init__(self) -> None:
        super().__init__()

        OPENAPI_ENABLE = False

        _ollama_raw = os.environ.get("OLLAMA_ENDPOINTS")
        self.OLLAMA_ENDPOINTS = json.loads(_ollama_raw)
