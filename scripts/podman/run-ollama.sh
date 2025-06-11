#!/bin/bash

set -euo pipefail

# 启动 Ollama 容器，并配置以下参数：
# 1. 移除了 GPU 加速，云服务器没有 GPU，因此不需要设备挂载
#    --device nvidia.com/gpu=all
# 2. --name 设置容器名称为 ollama
# 3. --replace 如果已有同名容器，则将其替换
# 4. --restart=always 容器意外退出后会自动重启
# 5. -v ollama:/root/.ollama:Z 持久化存储数据，并为 SELinux 自动打标签，确保容器能够安全访问挂载目录
# 6. -p 11434:11434 将主机的端口 11434 映射到容器的 11434（Ollama 默认使用的端口）
#    --network twila_network 代替 -p
# 7. docker.io/ollama/ollama 使用官方的 Ollama 镜像（如果本地没有镜像，将从 Docker Hub 自动拉取）
podman run -d $NETWORK_ARG \
        --replace \
	--name ollama \
	--replace \
	--restart=always \
	-v ollama:/root/.ollama:Z \
	docker.io/ollama/ollama

# 拉取模型,使用最小的模型
podman exec -i ollama ollama pull qwen2.5:0.5b

# 查看下载了那些 podman ollama 模型
podman exec -i ollama ollama list
