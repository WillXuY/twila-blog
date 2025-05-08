#!/usr/bin/env bash
set -euo pipefail
trap 'unset DATABASE_URL SECRET_KEY' EXIT

# 配置
: "${CONTAINER_NAME:=twila-blog}"
: "${IMAGE:=quay.io/willxuy/twila-blog:v0.1.0-build.1-20250507}"
: "${PORT:=5000}"
: "${NETWORK:=twila-network}"

#—— 检查 .env.gpg ——#
# 所需内容： 密码在 ../postgresql/init_database.sql 里设置了
# DATABASE_URL=postgresql://<User>:<Pwd>@pgsql:5432/<Database>
# SECRET_KEY= 这里使用工具或者自行随机生成一个密码
[[ -f .env.gpg ]] || { echo "⛔ .env.gpg 不存在" >&2; exit 1; }

#—— 解密并导出变量 ——#
while IFS='=' read -r key val; do
  [[ -z "$key" || "$key" =~ ^# ]] && continue
  [[ "$key" =~ ^[A-Z_][A-Z0-9_]*$ ]] || {
    echo "⛔ 无效变量名：$key" >&2; exit 1
  }
  export "$key"="$val"
done < <(gpg --batch --quiet --decrypt .env.gpg)

#—— 网络 ——#
if ! podman network exists "$NETWORK"; then
  podman network create "$NETWORK"
fi

#—— 启动容器 ——#
echo "🚀 启动 Flask 容器：$CONTAINER_NAME"
podman run -d \
  --replace \
  --name "$CONTAINER_NAME" \
  --network "$NETWORK" \
  -p "$PORT:$PORT" \
  -e DATABASE_URL \
  -e SECRET_KEY \
  "$IMAGE"
