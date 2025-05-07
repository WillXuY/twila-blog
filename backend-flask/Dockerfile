# 这个镜像基于 RHEL8
FROM quay.io/sclorg/python-311-minimal-el8

ARG VERSION
LABEL maintainer="willxuy <will.xu.work@zohomail.com>"
LABEL version=${VERSION}
LABEL changelog="${VERSION}: Add history for AI chat."
LABEL description="A Flask-based blog with AI chat homepage."

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple --no-cache-dir -r requirements.txt

COPY . /app

CMD ["python", "wsgi.py"]
