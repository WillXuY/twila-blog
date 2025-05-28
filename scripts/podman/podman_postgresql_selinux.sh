#!/usr/bin/env bash
set -euo pipefail
trap 'unset POSTGRES_USER POSTGRES_PASSWORD POSTGRES_DB NETWORK_ARG PGDATA_DIR PG_CONTAINER_NAME PG_IMAGE' EXIT

# 必须全部通过环境变量传入，无默认值
: "${PGDATA_DIR:?请设置环境变量 PGDATA_DIR}"
: "${PG_CONTAINER_NAME:?请设置环境变量 PG_CONTAINER_NAME}"
: "${PG_IMAGE:?请设置环境变量 PG_IMAGE}"

# 环境变量检查
[[ -n "$POSTGRES_USER" && -n "$POSTGRES_PASSWORD" && -n "$POSTGRES_DB" ]] || {
  echo "⛔ POSTGRES_* 环境变量不完整" >&2
  exit 1
}

# 准备数据目录
mkdir -p "$PGDATA_DIR"
chmod a+X "$(dirname "$PGDATA_DIR")"

# 启动容器
if podman container exists "$PG_CONTAINER_NAME"; then
  echo "📦 容器已存在，尝试启动..."
  podman start "$PG_CONTAINER_NAME"
else
  echo "📦 创建并启动容器..."
  podman run -d $NETWORK_ARG \
    --name "$PG_CONTAINER_NAME" \
    -e POSTGRES_USER="$POSTGRES_USER" \
    -e POSTGRES_PASSWORD="$POSTGRES_PASSWORD" \
    -e POSTGRES_DB="$POSTGRES_DB" \
    -v "$PGDATA_DIR":/var/lib/postgresql/data:Z \
    -p 127.0.0.1:5432:5432 \
    "$PG_IMAGE"
fi
