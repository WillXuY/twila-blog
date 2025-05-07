from flask import Blueprint, request, Response, stream_with_context, jsonify
import requests
import json
import logging
import uuid
from application.models import Conversation, Message, db

chat_bp = Blueprint('chat', __name__)
logger = logging.getLogger(__name__)
# Configure logger to output to console
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

OLLAMA_API_URL = "http://ollama:11434/api/chat"

def handle_message(user_id, conversation_id, user_message, model="qwen2.5:0.5b"):
    logger.debug(f"handle_message called with user_id={user_id}, conversation_id={conversation_id}, message={user_message}")
    # 校验 user_id
    try:
        uid = uuid.UUID(user_id)
    except Exception as e:
        logger.error(f"Invalid user_id: {e}")
        raise ValueError("Invalid user_id")

    # 1) 获取或创建会话
    if conversation_id:
        try:
            cid = uuid.UUID(conversation_id)
            conv = Conversation.query.get(cid)
            if not conv:
                raise ValueError("Conversation not found")
        except Exception:
            logger.debug("Creating new conversation due to invalid or missing conversation_id")
            conv = Conversation(user_id=uid, title=user_message[:20])
            db.session.add(conv)
            db.session.commit()
    else:
        conv = Conversation(user_id=uid, title=user_message[:20])
        db.session.add(conv)
        db.session.commit()
    conv_id = conv.id
    logger.debug(f"Using conversation_id={conv_id}")

    # 2) 插入用户消息
    user_msg = Message(conversation_id=conv_id, role='user', content=user_message)
    db.session.add(user_msg)
    db.session.commit()
    logger.debug(f"Inserted user message id={user_msg.id}")

    # 3) 构造 AI 请求
    payload = {
        "model": model,
        "stream": True,
        "messages": [{"role": "user", "content": user_message}]
    }

    full_reply_chunks = []

    def ai_generator():
        logger.debug("AI generator started")
        try:
            with requests.post(OLLAMA_API_URL, json=payload, stream=True) as r:
                r.raise_for_status()
                for line in r.iter_lines(decode_unicode=True):
                    if not line.strip():
                        continue
                    try:
                        chunk = json.loads(line)
                        content = chunk.get("message", {}).get("content", "")
                    except Exception as e:
                        logger.error(f"Error parsing AI chunk: {e}")
                        continue

                    if content:
                        full_reply_chunks.append(content)
                        yield content
        finally:
            # 4) AI 完整回复后插入数据库，并更新会话标题为首条用户消息摘录
            full_reply = "".join(full_reply_chunks)
            logger.debug(f"Full AI reply: {full_reply}")
            try:
                ai_msg = Message(conversation_id=conv_id, role='assistant', content=full_reply)
                db.session.add(ai_msg)
                # 更新会话标题为用户输入的节选
                conv.title = user_message[:20]
                db.session.commit()
                logger.debug(f"Inserted assistant message id={ai_msg.id} and updated convo title to {conv.title}")
            except Exception as e:
                logger.error(f"Failed to insert assistant message: {e}")

    return conv_id, ai_generator()

@chat_bp.route('', methods=['POST'])
def chat():
    data = request.get_json() or {}
    user_id = data.get('user_id')
    conversation_id = data.get('conversation_id')
    user_message = data.get('message', '').strip()

    logger.debug(f"/chat request received: {data}")

    if not user_id or not user_message:
        error_msg = "user_id and message are required"
        logger.error(error_msg)
        return jsonify({"error": error_msg}), 400

    try:
        conv_id, generator = handle_message(user_id, conversation_id, user_message)
    except ValueError as e:
        logger.error(f"ValueError in handle_message: {e}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logger.exception("Unexpected error in handle_message")
        return jsonify({"error": "Internal server error"}), 500

    headers = {"X-Conversation-Id": str(conv_id)}
    logger.debug(f"Returning response with conversation_id header={conv_id}")
    return Response(stream_with_context(generator), content_type='text/plain', headers=headers)
