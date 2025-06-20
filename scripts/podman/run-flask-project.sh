#!/usr/bin/env bash
set -euo pipefail

: "${CONTAINER_NAME:=twila-blog}"
: "${PORT:=5000}"
: "${NETWORK:=twila-network}"
: "${IMAGE:=quay.io/willxuy/twila-blog:$VERSION}"

# 检查环境变量
[[ -z "${DATABASE_URL:-}" || -z "${SECRET_KEY:-}" ]] && {
  echo "⛔ 缺少数据库配置环境变量"
  exit 1
}

echo "🚀 启动 Flask 容器：$CONTAINER_NAME"
podman run -d \
  --replace \
  --name "$CONTAINER_NAME" \
  --network "$NETWORK" \
  -p "127.0.0.1:$PORT:$PORT" \
  -e DATABASE_URL \
  -e SECRET_KEY \
  -e OLLAMA_ENDPOINTS \
  "$IMAGE"
