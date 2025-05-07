#!/bin/bash

# 创建一个公共网络
podman network create twila-network

# 存放 .env 的位置
sudo mkdir -p /etc/twila-blog
sudo vi /etc/twila-blog/.env

# 只需要创建目录和设置权限，其他操作不需要执行
sudo chmod 755 /etc/twila-blog
sudo chmod 644 /etc/twila-blog/.env

# 获取数据库的ip
sudo podman inspect -f '{{.NetworkSettings.IPAddress}}' pgsql

# 所需内容： 密码在 ../postgresql/init_database.sql 里设置了
# DATABASE_URL=postgresql://<User>:<Pwd>@<IP>:5432/<Database>
# SECRET_KEY= 这里使用工具或者自行随机生成一个密码

# 最后的 version 在 flask 项目根目录
podman run -d \
  --replace \
  --name twila-blog \
  -v /etc/twila-blog/.env:/app/application/.env:ro \
  --network twila-network \
  -p 5000:5000 \
  quay.io/willxuy/twila-blog:v0.1.0-build.1-20250507
