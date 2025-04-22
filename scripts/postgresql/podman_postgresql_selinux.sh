#!/bin/bash

# 让 gpg 不要调用图形化处理
export GPG_TTY=$(tty)

# 🐘 容器镜像配置
PG_IMAGE="quay.io/sclorg/postgresql-15-c9s"
PG_CONTAINER_NAME="pgsql"

# 📁 容器数据存储路径（推荐 /var/lib/containers 为符合 SELinux 的默认目录）
PGDATA_DIR="/var/lib/containers/pgdata"

# 🔧 创建持久化目录
echo "📂 创建数据目录：$PGDATA_DIR"
sudo mkdir -p "$PGDATA_DIR"

# Debian 需要额外配置目录权限给容器内用户使用
# 获取容器内 postgres 用户和组的 UID/GID
PG_UID=$(sudo podman run --rm "$PG_IMAGE" id -u postgres)
PG_GID=$(sudo podman run --rm "$PG_IMAGE" id -g postgres)
# 修改宿主机目录属主属组
sudo chown -R "${PG_UID}:${PG_GID}" "$PGDATA_DIR"
# 设置目录权限为 700（仅 owner 可读写执行）
sudo chmod 700 "$PGDATA_DIR"

# 获取发行版信息，跳过 debian 的 SELinux 的上下文判断
DISTRO=$(lsb_release -si)

if [[ "$DISTRO" == "Debian" ]]; then
	echo "Skip SELinux setting"
else
	# 🔒 设置 SELinux 上下文类型为 container_file_t（Podman 推荐）
	echo "🔐 设置 SELinux 上下文类型为 container_file_t"
	# 默认目录，放在 /var/lib/containers/ 下不需要设置上下文。
	sudo semanage fcontext -a -t container_file_t "${PGDATA_DIR}(/.*)?"
	sudo restorecon -Rv "$PGDATA_DIR"
fi

# 🚀 启动 PostgreSQL 容器（Podman）
echo "🚀 启动 PostgreSQL 容器..."

#!/usr/bin/env bash
# 开启严格模式
set -o errexit
set -o nounset
set -o pipefail

# 使用变量接收解密内容，避免硬盘临时文件
# 若解密失败，脚本会立即退出
decrypted=$(gpg --quiet --decrypt .env.gpg)

# 安全解析并导出环境变量
while IFS='=' read -r key val; do
  # 跳过空行和注释
  [[ -z "$key" || "$key" =~ ^# ]] && continue
  # 验证键名仅允许大写字母、数字和下划线
  if [[ "$key" =~ ^[A-Z_][A-Z0-9_]*$ ]]; then
    export "$key"="$val"
  else
    echo "无效的环境变量名：$key" >&2
    unset decrypted
    exit 1
  fi
done <<< "$decrypted"
# 清理解密内容变量
unset decrypted

# 校验关键变量是否已设置
: "${POSTGRESQL_USER:?POSTGRESQL_USER 未设置，退出执行！}"
: "${POSTGRESQL_PASSWORD:?POSTGRESQL_PASSWORD 未设置，退出执行！}"
: "${POSTGRESQL_DB:?POSTGRESQL_DB 未设置，退出执行！}"
: "${PGDATA_DIR:?PGDATA_DIR 未设置，退出执行！}"
: "${PG_CONTAINER_NAME:?PG_CONTAINER_NAME 未设置，退出执行！}"
: "${PG_IMAGE:?PG_IMAGE 未设置，退出执行！}"

# 使用 --env 直接传递环境变量，避免使用硬盘文件
sudo --preserve-env=PGDATA_DIR podman run -d \
  --name "$PG_CONTAINER_NAME" \
  -e POSTGRESQL_USER="$POSTGRESQL_USER" \
  -e POSTGRESQL_PASSWORD="$POSTGRESQL_PASSWORD" \
  -e POSTGRESQL_DATABASE="$POSTGRESQL_DB" \
  -v "${PGDATA_DIR}:/var/lib/pgsql/data:Z" \
  -p 5432:5432 \
  "$PG_IMAGE"

# 清理敏感环境变量
unset POSTGRESQL_USER POSTGRESQL_PASSWORD POSTGRESQL_DB

# 检查容器是否启动成功
if sudo podman ps -a | grep -q "$PG_CONTAINER_NAME"; then
	echo "✅ 容器已启动并持久化数据至 ${PGDATA_DIR}"
else
	echo "❌ 启动容器失败，请检查日志。"
fi
