"""
项目的启动脚本

使用方法：
# 生产环境启动（默认）
python3 start_project_optional.py --env prod
# 开发环境启动，端口映射到localhost
python3 start_project_optional.py --env dev
# 只重启 flask 的参数
python3 start_project_optional.py --env dev --flask-only
"""

import subprocess
import argparse
import os

from config import NETWORK_NAME, get_ollama_config, get_postgres_config, get_flask_config


def create_network(network_name: str):
    result = subprocess.run(["podman", "network", "exists", network_name])
    if result.returncode != 0:
        print(f"Network {network_name} does not exist, creating...")
        subprocess.run(["podman", "network", "create", network_name], check=True)
    else:
        print(f"Network {network_name} already exists.")


def run_shell_script(script_path: str, config: dict):
    print(f"Running script: {script_path} with config keys: {list(config.keys())}")
    env_vars = os.environ.copy()
    # 将 config 中所有键值加入环境变量
    for k, v in config.items():
        env_vars[k] = v
    subprocess.run(["/bin/bash", script_path], check=True, env=env_vars)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="启动项目容器")
    parser.add_argument("--env", choices=["dev", "prod"], default="prod", help="环境类型，默认为prod")
    parser.add_argument("--flask-only", action="store_true", help="仅启动 Flask 服务，跳过 Ollama 和 PostgreSQL")

    args = parser.parse_args()
    env = args.env
    flask_only = args.flask_only

    if not flask_only:
        if env != "dev":
            create_network(NETWORK_NAME)

        run_shell_script("./podman/get-start-ollama.sh", get_ollama_config(env))
        run_shell_script("./podman/podman_postgresql_selinux.sh", get_postgres_config(env))

    print("注意！首次运行时找到 run-flask-dev.sh 脚本把里面的安装依赖这一行解除注释，安装必要的依赖！")
    # 启动 Flask 服务（无论是否 flask_only）
    flask_script = "./run-flask-dev.sh" if env == "dev" else "./podman/run-flask-project.sh"
    run_shell_script(flask_script, get_flask_config(env))
