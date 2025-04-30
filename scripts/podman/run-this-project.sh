#!/bin/bash

# 与 ollama 协作需要创建一个公共网络
podman network create twila_network

podman run -d \
  --name twila-blog \
  --network twila_network \
  -p 5000:5000 \
  quay.io/willxuy/twila-blog:v0.0.0-build.0-20250430
