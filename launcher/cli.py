import questionary

from start_manager.dev import start_dev
from start_manager.prod import start_prod

ENV_DEV = "开发环境 dev"
ENV_PROD = "生产环境 prod"


def main() -> None:
    env_choice = questionary.select(
        "请选择启动模式: ",
        choices=[
            ENV_DEV,
            ENV_PROD,
        ]
    ).ask()

    if env_choice == ENV_DEV:
        start_dev.run()
    elif env_choice == ENV_PROD:
        start_prod.run()


if __name__ == "__main__":
    main()
