from .base import APP_ENV
from .dev import DevConfig
from .prod import ProdConfig

CONFIG_MAP = {
    APP_ENV.DEVELOPMENT.value: DevConfig,
    APP_ENV.PRODUCTION.value: ProdConfig,
}
