import questionary

from . import start_all
from . import start_web

START_WEB_ONLY = "只启动 web 项目"
START_ALL = "启动完整的数据库, ollama 和 web 项目"


def run() -> None:
    web_only_choice = questionary.select(
        "请选择启动模块: ",
        choices=[
            START_WEB_ONLY,
            START_ALL,
        ]
    ).ask()

    if web_only_choice == START_WEB_ONLY:
        start_web.run()
    elif web_only_choice == START_ALL:
        start_all.run()


if __name__ == "__main__":
    run()
