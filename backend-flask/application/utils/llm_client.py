import time
import json
import logging
import requests
from flask import current_app

logger = logging.getLogger(__name__)

class AIClientError(Exception):
    pass

def _post_streaming(endpoint, user_message, timeout_connect=10):
    """向单个 endpoint 发起 stream=True 的请求，返回 Response 对象"""
    payload = {
        "model": endpoint["model"],
        "stream": True,
        "messages": [{"role": "user", "content": user_message}]
    }
    r = requests.post(endpoint["url"], json=payload, stream=True, timeout=timeout_connect)
    r.raise_for_status()
    return r

def stream_response(user_message, connect_timeout=10, idle_timeout=10):
    """
    依次尝试 config 中的每个 Ollama endpoint，
    对流返回进行 idle_timeout 秒的“无数据断开”检测，失败则切下一个模型。
    最终 yield content chunk by chunk。
    """
    endpoints = current_app.config["OLLAMA_ENDPOINTS"]
    last_exc = None

    for ep in endpoints:
        try:
            logger.debug(f"[AIClient] trying {ep['model']} @ {ep['url']}")
            r = _post_streaming(ep, user_message, timeout_connect=connect_timeout)

            start = time.time()
            for line in r.iter_lines(decode_unicode=True):
                if not line.strip():
                    continue
                start = time.time()

                try:
                    data = json.loads(line)
                    content = data.get("message", {}).get("content", "")
                except Exception as e:
                    logger.error(f"[AIClient] parse error: {e}")
                    continue

                if content:
                    yield content

                if time.time() - start > idle_timeout:
                    raise TimeoutError(f"idle for {idle_timeout}s on {ep['model']}")
            # 正常读完流，则结束所有尝试
            return

        except Exception as e:
            logger.warning(f"[AIClient] endpoint {ep['url']} failed: {e}")
            last_exc = e
            # 继续尝试下一个 endpoint

    # 所有 endpoint 都失败
    raise AIClientError(f"All AI endpoints failed: {last_exc}")
