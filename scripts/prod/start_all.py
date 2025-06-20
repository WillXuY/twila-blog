from pathlib import Path

from .config import ProdConfig, INIT_DATABASE_SQL
from .start_web import run as run_web
from ..common.utils import run_script

# 定位要运行的脚本的所在目录
PODMAN_SCRIPT_PATH = Path(__file__).resolve().parents[1] / "podman"
PGSQL_SCRIPT = PODMAN_SCRIPT_PATH / "run-pgsql.sh"
OLLAMA_SCRIPT = PODMAN_SCRIPT_PATH / "run-ollama.sh"


def init_database() -> None:
    print("\n⚠️  注意: 数据库初始化需要手动完成。")
    print("请参考以下 SQL 脚本完成数据库和表的创建: ")
    print(f"  1. 数据库和用户创建脚本: {INIT_DATABASE_SQL}")
    print("  2. 表结构创建脚本: /path/to/twila-blog/scripts/postgresql/create_tables.sql")
    print("\n请根据需要修改密码等信息后执行，例如: ")
    print("  $ podman exec -it pgsql psql -U postgres -f /path/to/init_database.sql")
    print("  $ podman exec -it pgsql psql -U twila_admin -d twila_blog -f /path/to/create_tables.sql\n")


def run(config: ProdConfig) -> None:
    pgsql_config = config.get_postgres_config()
    run_script(str(PGSQL_SCRIPT), env_vars=pgsql_config)
    ollama_config = config.get_ollama_config()
    run_script(str(OLLAMA_SCRIPT), env_vars=ollama_config)

    init_database()
    run_web(config)


if __name__ == "__main__":
    run(ProdConfig())
