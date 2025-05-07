import os
import subprocess
from io import StringIO
from dotenv import dotenv_values

class Config:
    @staticmethod
    def load_secrets():
        env_gpg_path = os.path.join(os.path.dirname(__file__), ".env.gpg")
        try:
            decrypted = subprocess.check_output(
                ["gpg", "--quiet", "--decrypt", env_gpg_path],
                text=True
            )
            return dotenv_values(stream=StringIO(decrypted))
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to decrypt .env.gpg: {e}") from e

    secrets = load_secrets.__func__()  # 类加载时调用一次

    # Flask 配置项
    SQLALCHEMY_DATABASE_URI = secrets.get("DATABASE_URL", "")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = secrets.get("SECRET_KEY", "fallback-secret")
