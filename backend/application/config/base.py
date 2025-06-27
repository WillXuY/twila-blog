"""
提供基础的公共配置内容,
由 dev test prod 等环境继承共用.
"""

from enum import Enum


class APP_ENV(Enum):
    DEVELOPMENT = "dev"
    TESTING = "test"
    PRODUCTION = "prod"


class BaseConfig:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
