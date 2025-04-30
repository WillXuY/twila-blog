#!/bin/bash

# 版本号需要及时修改
podman build -t quay.io/willxuy/twila-blog:v0.0.0-build.0-20250430 .

# push to origin quay io
podman login quay.io
podman push quay.io/willxuy/twila-blog:v0.0.0-build.0-20250430
