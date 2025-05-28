from flask import Blueprint, request, Response, stream_with_context, jsonify

from application.services.chat_service import handle_chat, get_conversations, get_conversation_messages

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('', methods=['POST'])
def chat():
    data = request.get_json() or {}
    user_id      = data.get('user_id')
    conv_id_str  = data.get('conversation_id')
    user_message = data.get('message', '').strip()

    if not user_id:
        return jsonify({"error": "user_id are required"}), 400
    if not user_message:
        return jsonify({"error": "user_message are required"}), 400

    return handle_chat(user_id, conv_id_str, user_message)

@chat_bp.route('/conversations', methods=['GET'])
def list_conversations():
    user_id = request.args.get('user_id')
    return get_conversations(user_id)

@chat_bp.route('/conversations/<conversation_id>/messages', methods=['GET'])
def get_messages(conversation_id):
    user_id = request.args.get('user_id')
    return get_conversation_messages(user_id, conversation_id)
