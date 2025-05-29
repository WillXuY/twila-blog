import subprocess

COMMAND_REQUIRED = {"podman": "--version", "gpg": "--list-keys"}


def check_command_exists(cmd: str, arg: str) -> bool:
    """检查命令是否可用"""
    try:
        subprocess.run([cmd, arg], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def check_tools_ready() -> None:
    """检查必要的软件和对应的功能是否存在, 不检查 bash 内建功能，默认 chmod/mkdir 等 coreutils 存在。"""
    missing = [f"{cmd} {arg}" for cmd, arg in COMMAND_REQUIRED.items() if not check_command_exists(cmd, arg)]
    if missing:
        print(f"缺少必备功能: {', '.join(missing)}，请先安装或配置。")
        exit(1)


def main() -> None:
    print("校验必要功能是否已就绪...(默认 bash 环境，不校验 bash 内建功能，Windows 兼容性很低！谨慎使用！)")
    check_tools_ready()
    print("所有必备命令和功能已安装，准备启动。")


if __name__ == "__main__":
    main()
