from application.models.conversations import Conversation
from application.models.messages import Message
from application.extensions import db


def save_user_message(conversation_id, content):
    msg = Message(conversation_id=conversation_id, role='user', content=content)
    db.session.add(msg)
    db.session.commit()


def save_assistant_message(conversation_id, reply, conv, title_hint):
    msg = Message(conversation_id=conversation_id, role='assistant', content=reply)
    db.session.add(msg)
    conv.title = title_hint[:20]  # 可略作更新
    db.session.commit()


def get_messages_for_conversation(user_id, conv_id):
    conv = Conversation.query.get(conv_id)
    if not conv or conv.user_id != user_id:
        return []

    msgs = (
        Message.query
        .filter_by(conversation_id=conv_id)
        .order_by(Message.created_at.asc())
        .all()
    )
    return [
        {"role": m.role, "content": m.content, "created_at": m.created_at.isoformat()}
        for m in msgs
    ]
