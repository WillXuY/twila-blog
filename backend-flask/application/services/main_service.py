import threading

from flask import Flask

from application.utils.ollama_preheat import preheat_ollama_models

def start_ollama_preheat(app: Flask):
    """以非阻塞方式启动模型预热"""
    threading.Thread(target=preheat_ollama_models, args=(app,), daemon=True).start()
