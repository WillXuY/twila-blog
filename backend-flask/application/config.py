import os
from dotenv import dotenv_values

class Config:
    @staticmethod
    def load_secrets():
        env_path = os.path.join(os.path.dirname(__file__), ".env")
        # 直接加载 .env 文件内容
        return dotenv_values(env_path)

    secrets = load_secrets.__func__()  # 类加载时调用一次

    # Flask 配置项
    SQLALCHEMY_DATABASE_URI = secrets.get("DATABASE_URL", "")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = secrets.get("SECRET_KEY", "fallback-secret")
