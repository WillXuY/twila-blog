from pathlib import Path

from . import config
from ..common.utils import run_script


def run() -> None:
    flask_config = config.get_flask_config()
    flask_script_path = Path(__file__).parent / "run-flask.sh"
    run_script(str(flask_script_path), env_vars=flask_config)


if __name__ == "__main__":
    run()
