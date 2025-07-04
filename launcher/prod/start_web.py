from config.factory import get_service_configs
from utils.run import run_script
from pathlib import Path
import os

# 获取 Flask 脚本路径
SCRIPT_PATH = Path(__file__).parents[2] / "scripts" / "podman" / "run-flask-project.sh"


def run(env: str = "prod") -> None:
    services = get_service_configs(env)
    flask_env = services["flask"]

    env_vars = os.environ.copy()
    env_vars.update(flask_env)

    print("🚀 启动 Flask 容器，使用环境配置：")
    for k, v in flask_env.items():
        print(f"{k}={v}")

    run_script(str(SCRIPT_PATH), env_vars=env_vars)
