#!/bin/bash
set -e

VERSION=$(cat ../../backend-flask/VERSION)
IMAGE_NAME="quay.io/willxuy/twila-blog:$VERSION"

echo "Building image: $IMAGE_NAME"
echo "Reading VERSION: $VERSION"

# 版本号需要及时修改
podman build --build-arg VERSION="$VERSION" -t "$IMAGE_NAME" ../../backend-flask
