from flask import Blueprint, request, Response, stream_with_context
import requests, json

chat_bp = Blueprint('chat', __name__)

# 这里采用了内部网络调用，不能使用 localhost
OLLAMA_API_URL = "http://localhost:11434/api/chat"

@chat_bp.route('', methods=['POST'])
def chat():
    user_message = request.json.get('message', '')

    payload = {
        "model": "qwen2.5:0.5b",  # 修改为你实际使用的模型
        "stream": True,
        "messages": [{"role": "user", "content": user_message}]
    }

    def generate():
        with requests.post(OLLAMA_API_URL, json=payload, stream=True) as r:
            for line in r.iter_lines(decode_unicode=True):
                if line.strip():
                    try:
                        chunk = json.loads(line)
                        content = chunk.get("message", {}).get("content", "")
                        if content:
                            yield content
                    except Exception as e:
                        yield f"[Error parsing]: {e}"

    return Response(stream_with_context(generate()), content_type='text/plain')
