#!/usr/bin/env bash
set -euo pipefail
trap 'unset POSTGRES_USER POSTGRES_PASSWORD POSTGRES_DB' EXIT

#—— 基础配置 ——#
# 手动下载一个 docker hub 的 postgres 然后上传到 quay
: "${XDG_DATA_HOME:=$HOME/.local/share}"
: "${PGDATA_DIR:=$XDG_DATA_HOME/containers/postgres/data}"
: "${PG_CONTAINER_NAME:=pgsql}"
: "${PG_IMAGE:=quay.io/willxuy/postgres:latest}"
: "${ENV_FILE_ENC:=.env.gpg}"

echo "🚀 启动 PostgreSQL 容器..."
echo "    数据目录 PGDATA_DIR=$PGDATA_DIR"

#—— 1) 校验 .env.gpg ——#
[[ -f "$ENV_FILE_ENC" ]] || {
  echo "⛔ 未找到加密环境文件：$ENV_FILE_ENC" >&2
  exit 1
}

#—— 2) 准备数据目录 ——#
mkdir -p "$PGDATA_DIR"
chmod a+X "$(dirname "$PGDATA_DIR")"

#—— 3) 解密环境变量 ——#
while IFS='=' read -r key val; do
  [[ -z "$key" || "$key" =~ ^# ]] && continue
  [[ "$key" =~ ^[A-Z_][A-Z0-9_]*$ ]] || {
    echo "⛔ 无效变量：$key" >&2
    exit 1
  }
  export "$key"="$val"
done < <(gpg --batch --quiet --decrypt "$ENV_FILE_ENC")

#—— 4) 环境变量兼容处理 ——#
: "${POSTGRES_USER:=${POSTGRESQL_USER:-}}"
: "${POSTGRES_PASSWORD:=${POSTGRESQL_PASSWORD:-}}"
: "${POSTGRES_DB:=${POSTGRESQL_DB:-}}"

[[ -n "$POSTGRES_USER" && -n "$POSTGRES_PASSWORD" && -n "$POSTGRES_DB" ]] || {
  echo "⛔ POSTGRES_* 环境变量不完整" >&2
  exit 1
}

#—— 5) 网络 ——#
if ! podman network exists twila-network; then
  podman network create twila-network
fi

#—— 6) 启动容器 ——#
if podman container exists "$PG_CONTAINER_NAME"; then
  echo "📦 容器已存在，尝试启动..."
  podman start "$PG_CONTAINER_NAME"
else
  echo "📦 创建并启动容器..."
  podman run -d \
    --name "$PG_CONTAINER_NAME" \
    --network twila-network \
    -e POSTGRES_USER="$POSTGRES_USER" \
    -e POSTGRES_PASSWORD="$POSTGRES_PASSWORD" \
    -e POSTGRES_DB="$POSTGRES_DB" \
    -v "$PGDATA_DIR":/var/lib/postgresql/data:Z \
    -p 127.0.0.1:5432:5432 \
    "$PG_IMAGE"
fi
