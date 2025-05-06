#!/bin/bash

podman run -d \
  --name twila-blog \
  -p 5000:5000 \
  quay.io/willxuy/twila-blog:v0.0.0-build.0-20250430
