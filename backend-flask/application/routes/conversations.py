# application/routes/conversations.py
from flask import Blueprint, request, jsonify
import uuid
from application.models import Conversation

conversations_bp = Blueprint('conversations', __name__)

@conversations_bp.route('', methods=['GET'])
def list_conversations():
    user_id = request.args.get('user_id')
    try:
        uid = uuid.UUID(user_id)
    except Exception:
        return jsonify({"history": []}), 200

    convs = (
        Conversation.query
        .filter_by(user_id=uid)
        .order_by(Conversation.updated_at.desc())
        .limit(20)
        .all()
    )
    return jsonify({
        "history": [
            {"id": str(c.id), "title": c.title, "updated_at": c.updated_at.isoformat()}
            for c in convs
        ]
    }), 200
