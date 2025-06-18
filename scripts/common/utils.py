import subprocess
import os

from typing import Optional, Dict


def check_command_exists(cmd: str, arg: str) -> bool:
    """检查命令是否可用"""
    try:
        subprocess.run([cmd, arg], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def check_tools_ready(COMMAND_REQUIRED: dict[str, str]) -> None:
    """检查必要的软件和对应的功能是否存在, 不检查 bash 内建功能，默认 chmod/mkdir 等 coreutils 存在。"""
    missing = [f"{cmd} {arg}" for cmd, arg in COMMAND_REQUIRED.items() if not check_command_exists(cmd, arg)]
    if missing:
        print(f"缺少必备功能: {', '.join(missing)}，请先安装或配置。")
        exit(1)


def run_script(script_path: str, env_vars: Optional[Dict[str, str]] = None) -> None:
    """调用外部 shell 脚本，并传入环境变量"""
    env = os.environ.copy()
    if env_vars:
        env.update(env_vars)

    print(f"启动脚本: {script_path}")
    result = subprocess.run(["bash", script_path], env=env)
    if result.returncode != 0:
        raise RuntimeError(f"脚本 {script_path} 执行失败，退出码 {result.returncode}")
