from pathlib import Path

from .config import ProdConfig
from ..common.utils import run_script

# 定位要运行的脚本的所在目录
PODMAN_SCRIPT_PATH = Path(__file__).resolve().parents[1] / "podman"
FLASK_SCRIPT = PODMAN_SCRIPT_PATH / "run-flask-project.sh"


def run(config: ProdConfig) -> None:
    flask_config = config.get_flask_config()
    run_script(str(FLASK_SCRIPT), env_vars=flask_config)


if __name__ == "__main__":
    run(ProdConfig())
