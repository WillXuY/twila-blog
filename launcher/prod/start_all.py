from config.factory import get_service_configs
from config.prod.config import ProdConfig
from utils.run import run_script
from pathlib import Path
import os

ROOT = Path(__file__).parents[2]
PG_SCRIPT = ROOT / "scripts" / "podman" / "run-pgsql.sh"
OLLAMA_SCRIPT = ROOT / "scripts" / "podman" / "run-ollama.sh"
FLASK_SCRIPT = ROOT / "scripts" / "podman" / "run-flask-project.sh"
INIT_DATABASE_SQL = ProdConfig.PROD_INIT_DATABASE_SQL_PATH


def init_database() -> None:
    print("\n⚠️  注意: 数据库初始化需要手动完成。")
    print("请参考以下 SQL 脚本完成数据库和表的创建: ")
    print(f"  1. 数据库和用户创建脚本: {INIT_DATABASE_SQL}")
    print("  2. 表结构创建脚本: /path/to/twila-blog/scripts/postgresql/create_tables.sql")
    print("\n请根据需要修改密码等信息后执行，例如: ")
    print("  $ podman exec -it pgsql psql -U postgres -f /path/to/init_database.sql")
    print("  $ podman exec -it pgsql psql -U twila_admin -d twila_blog -f /path/to/create_tables.sql\n")


def run(env: str = "prod") -> None:
    services = get_service_configs(env)
    pg_env = services["pg"]
    ollama_env = services["ollama"]
    flask_env = services["flask"]

    run_script(str(PG_SCRIPT), env_vars={**os.environ, **pg_env})
    run_script(str(OLLAMA_SCRIPT), env_vars={**os.environ, **ollama_env})
    run_script(str(FLASK_SCRIPT), env_vars={**os.environ, **flask_env})
    init_database()


if __name__ == "__main__":
    run(ProdConfig())
