# application/utils/model_preheat.py

import requests
import logging

logger = logging.getLogger(__name__)
_preheated = False

def preheat_ollama_models(app):
    """
    针对 alpaca 插件的 /api/chat 接口做预热：
    - stream=True
    - 只读到第一条数据就停止，标记预热完成
    """
    global _preheated
    if _preheated:
        return

    with app.app_context():
        for endpoint in app.config["OLLAMA_ENDPOINTS"]:
            url = endpoint["url"]  # 确保是 http://.../api/chat
            model = endpoint["model"]

            try:
                # 发起流式请求
                resp = requests.post(
                    url,
                    json={
                        "model": model,
                        "stream": True,
                        "messages": [{"role": "user", "content": "ping"}]
                    },
                    stream=True,
                    timeout=30
                )
                resp.raise_for_status()

                # 只消费第一条响应数据就视为加载成功
                for line in resp.iter_lines(decode_unicode=True):
                    if line and line.strip():
                        logger.info(f"[Preheat] got first chunk from {model}")
                        _preheated = True
                        break

                resp.close()
                if _preheated:
                    logger.info(f"[Preheat] successful for {model} at {url}")
                    break

            except Exception as e:
                logger.warning(f"[Preheat] failed for {model} at {url}: {e}")
