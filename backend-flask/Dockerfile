# 这个镜像基于 RHEL8
FROM quay.io/sclorg/python-311-minimal-el8

LABEL maintainer="willxuy <will.xu.work@zohomail.com>"
LABEL version="v0.0.0-build.0-20250430"
LABEL changelog="v0.0.0: Added AI chat interface on homepage."
LABEL description="A Flask-based blog with AI chat homepage."

WORKDIR /app
COPY . /app
RUN pip install -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple flask requests
CMD ["python", "hello-ai.py"]
