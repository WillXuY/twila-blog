import questionary

from start_manager.common.utils import check_tools_ready, ensure_network_exists
from start_manager.prod.config import ProdConfig, COMMAND_REQUIRED, PODMAN_NERWORK_NAME
from start_manager.prod.start_all import run as run_all
from start_manager.prod.start_web import run as run_web

START_WEB_ONLY = "只启动 web 项目"
START_ALL = "启动完整的数据库, ollama 和 web 项目"


def run() -> None:
    check_tools_ready(COMMAND_REQUIRED)

    config = ProdConfig()

    web_only_choice = questionary.select(
        "请选择启动模块: ",
        choices=[START_WEB_ONLY, START_ALL]
    ).ask()

    ensure_network_exists(PODMAN_NERWORK_NAME)
    if web_only_choice == START_WEB_ONLY:
        run_web(config)
    elif web_only_choice == START_ALL:
        run_all(config)


if __name__ == "__main__":
    run()
