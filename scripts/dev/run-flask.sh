#!/bin/bash
set -e

ENV_NAME=twila-blog
VENV_PATH="$HOME/.virtualenvs/$ENV_NAME"

if [ ! -d "$VENV_PATH" ]; then
    echo "虚拟环境不存在，正在创建..."
    python3 -m venv "$VENV_PATH"
fi

echo "激活虚拟环境..."
source "$VENV_PATH/bin/activate"

# 安装依赖（可选）
# pip install -r ../../backend-flask/requirements.txt

cd "$(dirname "$0")/../../backend-flask"
echo "启动 Flask 开发服务..."
python3 wsgi.py
