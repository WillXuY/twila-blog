import uuid
from flask import Response, jsonify, stream_with_context
from application.repositories.conversation_repo import (
    get_or_create_conversation, list_recent_conversations
)
from application.repositories.message_repo import (
    save_user_message, save_assistant_message, get_messages_for_conversation
)
from application.utils.llm_client import stream_response, AIClientError


def handle_chat(user_id, conv_id, user_message):
    conv = get_or_create_conversation(user_id, conv_id, user_message)

    save_user_message(conv.id, user_message)

    def generate():
        chunks = []
        try:
            for content in stream_response(user_message):
                chunks.append(content)
                yield content
        except AIClientError as e:
            yield f"[Error] {e}"
        finally:
            reply = "".join(chunks)
            save_assistant_message(conv.id, reply, conv, user_message)

    return Response(stream_with_context(generate()),
                    content_type='text/plain',
                    headers={"X-Conversation-Id": str(conv.id)})


def get_conversations(user_id):
    convs = list_recent_conversations(user_id)
    return jsonify({"history": convs})


def get_conversation_messages(user_id, conv_id):
    return jsonify({"messages": get_messages_for_conversation(user_id, conv_id)})
