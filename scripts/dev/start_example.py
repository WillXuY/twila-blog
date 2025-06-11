import config
import os
import subprocess

from typing import Optional, Dict
from dotenv import load_dotenv


def run_script(script_path: str, env_vars: Optional[Dict[str, str]] = None) -> None:
    """调用外部 shell 脚本，并传入环境变量"""
    env = os.environ.copy()
    if env_vars:
        env.update(env_vars)

    print(f"启动脚本: {script_path}")
    result = subprocess.run(["bash", script_path], env=env)
    if result.returncode != 0:
        raise RuntimeError(f"脚本 {script_path} 执行失败，退出码 {result.returncode}")


def init_database() -> None:
    print("\n⚠️  注意：数据库初始化需要手动完成。")
    print("请参考以下 SQL 脚本完成数据库和表的创建：")
    print("  1. 数据库和用户创建脚本：/path/to/twila-blog/scripts/postgresql/init_database.sql")
    print("  2. 表结构创建脚本：/path/to/twila-blog/scripts/postgresql/create_tables.sql")
    print("\n请根据需要修改密码等信息后执行，例如：")
    print("  $ podman exec -it pgsql psql -U postgres -f /path/to/init_database.sql")
    print("  $ podman exec -it pgsql psql -U twila_admin -d twila_blog -f /path/to/create_tables.sql\n")


def main() -> None:
    # 1. 读取 env.example 文件，加载环境变量（不覆盖已存在的）
    load_dotenv(dotenv_path="../../env.example", override=False)

    # 2. 从 config.py 获取配置
    pg_config = config.get_postgres_config()
    flask_config = config.get_flask_config()

    # 3. 启动 PostgreSQL 容器
    run_script("../podman/run-pgsql.sh", env_vars=pg_config)

    # 4. 启动 Ollama 容器
    # 传入 NETWORK_ARG，因为你的 ollama.sh 脚本用到了它
    ollama_env = {
        "NETWORK_ARG": pg_config.get("NETWORK_ARG", "")
    }
    run_script("../podman/run-ollama.sh", env_vars=ollama_env)

    init_database()

    # 5. 启动 Flask 服务
    # Flask 脚本内部激活虚拟环境，不需要额外传环境变量
    run_script("run-flask.sh", env_vars=flask_config)

    print("所有服务已启动")


if __name__ == "__main__":
    main()
