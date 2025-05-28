#!/bin/bash
set -e  # 一旦出错就退出

ENV_NAME=twila-blog
VENV_PATH="$HOME/.virtualenvs/$ENV_NAME"

if [ ! -d "$VENV_PATH" ]; then
    echo "虚拟环境不存在，正在创建..."
    python3 -m venv "$VENV_PATH"
fi

echo "激活虚拟环境..."
source "$VENV_PATH/bin/activate"

# 安装依赖（可选）
# pip install -r ../backend-flask/requirements.txt

echo "启动 Flask 开发服务..."
cd ../backend-flask
python3 wsgi.py
