# 这个镜像基于 RHEL8
FROM quay.io/sclorg/python-311-minimal-el8

ARG VERSION=dev
ARG BUILD_DATE
ARG COMMIT_SHA

LABEL maintainer="willxuy <will.xu.work@zohomail.com>"
LABEL version=${VERSION}
LABEL changelog="${VERSION}: Introduced a new index page with GitHub mascot link."
LABEL description="Twila update: Added a new landing page featuring a mascot and GitHub repository link."

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple --no-cache-dir -r requirements.txt

COPY . /app

CMD ["python", "wsgi.py"]
