SHELL := /bin/bash
VENV_DIR := ~/.virtualenvs/twila-blog
PYTHON := $(VENV_DIR)/bin/python

# tuna 相关: 可选，使用国内源来加速
venv:
	mkdir -p $(VENV_DIR)
	python3 -m venv $(VENV_DIR)
	$(PYTHON) -m pip install -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple --upgrade pip
	$(PYTHON) -m pip config set global.index-url https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple
	$(PYTHON) -m pip install -r requirements.txt

start:
	source $(VENV_DIR)/bin/activate && $(PYTHON) start.py

# 可选：清除虚拟环境
clean:
	rm -rf $(VENV_DIR)
