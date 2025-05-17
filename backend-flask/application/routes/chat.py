import requests, json, logging, uuid, time

from flask import Blueprint, request, Response, stream_with_context, jsonify, current_app

from application.models import Conversation, Message, db
from application.utils.ai_client import stream_response, AIClientError

chat_bp = Blueprint('chat', __name__)

logger = logging.getLogger(__name__)
# Configure logger to output to console
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

@chat_bp.route('', methods=['POST'])
def chat():
    data = request.get_json() or {}
    user_id      = data.get('user_id')
    conv_id_str  = data.get('conversation_id')
    user_message = data.get('message', '').strip()

    if not user_id or not user_message:
        return jsonify({"error": "user_id and message are required"}), 400

    # 1) 验证或创建会话
    try:
        uid = uuid.UUID(user_id)
    except Exception:
        return jsonify({"error": "Invalid user_id"}), 400

    if conv_id_str:
        try:
            cid  = uuid.UUID(conv_id_str)
            conv = Conversation.query.get(cid) or None
        except Exception:
            conv = None
    else:
        conv = None

    if not conv:
        conv = Conversation(user_id=uid, title=user_message[:20])
        db.session.add(conv)
        db.session.commit()
    conv_id = conv.id

    # 2) 存储用户消息
    db.session.add(Message(conversation_id=conv_id, role='user', content=user_message))
    db.session.commit()

    # 3) 准备流式 response
    def generator():
        chunks = []
        try:
            for content in stream_response(user_message):
                chunks.append(content)
                yield content
        except AIClientError as e:
            yield f"[Error] {e}"
        finally:
            # 4) 存储 AI 回复 并更新对话标题
            reply = ''.join(chunks)
            db.session.add(Message(conversation_id=conv_id, role='assistant', content=reply))
            conv.title = user_message[:20]
            db.session.commit()

    headers = {"X-Conversation-Id": str(conv_id)}
    return Response(stream_with_context(generator()),
                    content_type='text/plain',
                    headers=headers)
