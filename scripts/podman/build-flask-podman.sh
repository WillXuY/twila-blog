#!/bin/bash
set -e

VERSION=$(cat ../../backend-flask/VERSION)
BUILD_DATE=$(date -u +'%Y-%m-%dT%H:%M:%SZ')
COMMIT_SHA=$(git rev-parse --short HEAD)
IMAGE="quay.io/willxuy/twila-blog:$VERSION"

podman build \
  --build-arg VERSION="$VERSION" \
  --build-arg BUILD_DATE="$BUILD_DATE" \
  --build-arg COMMIT_SHA="$COMMIT_SHA" \
  -t "$IMAGE" \
  ../../backend-flask
