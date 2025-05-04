#!/bin/bash
# 开启严格模式
set -euo pipefail
# 在脚本退出（成功或失败）时清理敏感变量
trap 'unset POSTGRESQL_USER POSTGRESQL_PASSWORD POSTGRESQL_DB' EXIT

# 基础配置
: "${PGDATA_DIR:=/var/lib/containers/pgdata}"
: "${PG_CONTAINER_NAME:=pgsql}"
: "${PG_IMAGE:=quay.io/sclorg/postgresql-15-c9s}"

echo "🚀 启动 PostgreSQL 容器..."

# 校验文件的存在性
[[ -f .env.gpg ]] || { echo ".env.gpg 不存在" >&2; exit 1; }

# 创建持久化目录
sudo mkdir -p "$PGDATA_DIR"

# 最严格——不在脚本中保存完整明文，只在循环内逐行处理
while IFS='=' read -r key val; do
  [[ -z "$key" || "$key" =~ ^[[:space:]]*# ]] && continue
  if [[ "$key" =~ ^[A-Z_][A-Z0-9_]*$ ]]; then
    export "$key"="$val"
  else
    echo "无效的环境变量名：$key" >&2
    exit 1
  fi
done < <(gpg --batch --quiet --decrypt .env.gpg)

# 校验关键变量是否已设置
: "${POSTGRESQL_USER:?POSTGRESQL_USER 未设置，退出执行！}"
: "${POSTGRESQL_PASSWORD:?POSTGRESQL_PASSWORD 未设置，退出执行！}"
: "${POSTGRESQL_DB:?POSTGRESQL_DB 未设置，退出执行！}"

# 1️⃣ 首次初始化并预置 password_encryption
# 设置 SELinux 上下文类型为 container_file_t（Podman 推荐）
# 默认目录，放在 /var/lib/containers/ 下不需要设置上下文。

if [[ ! -f "$PGDATA_DIR/PG_VERSION" ]]; then
  echo "🚀 首次初始化+权限设置"
  sudo podman run --rm \
    --name init-"$PG_CONTAINER_NAME" \
    -e POSTGRESQL_USER="$POSTGRESQL_USER" \
    -e POSTGRESQL_PASSWORD="$POSTGRESQL_PASSWORD" \
    -e POSTGRESQL_DATABASE="$POSTGRESQL_DB" \
    -v "${PGDATA_DIR}:/var/lib/pgsql/data:Z" \
    "$PG_IMAGE" \
    bash -c '
      # 1) 触发官方 init 脚本，生成数据目录
      /usr/bin/true &&
      # 2) 获取容器内 postgres 用户 UID/GID
      PG_UID=$(id -u postgres) &&
      PG_GID=$(id -g postgres) &&
      # 3) 在宿主机上 chown/chmod（通过 podman 容器内命令作用于挂载目录）
      chown -R $PG_UID:$PG_GID /var/lib/pgsql/data &&
      chmod 700 /var/lib/pgsql/data
      # 4) （如果仍需要）手动修正 SELinux 上下文
      # chcon -t container_file_t /var/lib/pgsql/data
    '
  echo "✅ 数据目录已初始化，且已设置权限"
fi

# 2️⃣ 启动或重启持久化容器
if sudo podman ps -a --format '{{.Names}}' | grep -q "^$PG_CONTAINER_NAME\$"; then
  if sudo podman ps --format '{{.Names}}' | grep -q "^$PG_CONTAINER_NAME\$"; then
    echo "🔄 容器已运行，跳过启动"
  else
    echo "♻️ 容器已存在但未运行，启动它"
    sudo podman start "$PG_CONTAINER_NAME"
  fi
else
  echo "🚀 第一次正式启动 PostgreSQL 容器"
  sudo podman run -d \
    --name "$PG_CONTAINER_NAME" \
    -e POSTGRESQL_USER="$POSTGRESQL_USER" \
    -e POSTGRESQL_PASSWORD="$POSTGRESQL_PASSWORD" \
    -e POSTGRESQL_DATABASE="$POSTGRESQL_DB" \
    -v "${PGDATA_DIR}:/var/lib/pgsql/data:Z" \
    --restart unless-stopped \
    -p 5432:5432 \
    "$PG_IMAGE"
fi

unset POSTGRESQL_USER POSTGRESQL_PASSWORD POSTGRESQL_DB

# —————— 配置清理/追加 + 重启生效 ——————
CONF="$PGDATA_DIR/postgresql.conf"
# 先删除所有 password_encryption 行，再追加一行
echo "🔧 清理旧的 password_encryption 并追加 SCRAM"
sudo sed -i '/^password_encryption/d' "$CONF"
echo "password_encryption = 'scram-sha-256'" | sudo tee -a "$CONF" >/dev/null

echo "🔁 重启容器以加载新配置"
sudo podman restart "$PG_CONTAINER_NAME"

echo "✅ 配置已生效：password_encryption = 'scram-sha-256'"
echo
echo "📦 当前容器状态："
sudo podman ps
