# application/routes/messages.py
from flask import Blueprint, request, jsonify
import uuid
from application.models import Conversation, Message

messages_bp = Blueprint('messages', __name__)

@messages_bp.route('/<conversation_id>/messages', methods=['GET'])
def get_messages(conversation_id):
    user_id = request.args.get('user_id')
    try:
        uid = uuid.UUID(user_id)
        cid = uuid.UUID(conversation_id)
    except Exception:
        return jsonify({"messages": []}), 200

    conv = Conversation.query.get(cid)
    if not conv or conv.user_id != uid:
        return jsonify({"messages": []}), 200

    msgs = (
        Message.query
        .filter_by(conversation_id=cid)
        .order_by(Message.created_at.asc())
        .all()
    )
    return jsonify({
        "messages": [
            {"role": m.role, "content": m.content, "created_at": m.created_at.isoformat()}
            for m in msgs
        ]
    }), 200
