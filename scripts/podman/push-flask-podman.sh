#!/bin/bash
set -e

VERSION=$(cat ../../backend-flask/VERSION)
IMAGE_NAME="quay.io/willxuy/twila-blog:$VERSION"

# push to origin quay io
podman login quay.io
podman push "$IMAGE_NAME"
