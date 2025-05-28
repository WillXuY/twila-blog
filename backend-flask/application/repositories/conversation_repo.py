from application.models.conversations import Conversation
from application.extensions import db

def get_or_create_conversation(user_id, conv_id_str, title_hint):
    if conv_id_str:
        try:
            conv = Conversation.query.get(conv_id_str)
            if conv and conv.user_id == user_id:
                return conv
        except Exception:
            pass

    conv = Conversation(user_id=user_id, title=title_hint[:20])
    db.session.add(conv)
    db.session.commit()
    return conv


def list_recent_conversations(user_id):
    convs = (
        Conversation.query
        .filter_by(user_id=user_id)
        .order_by(Conversation.updated_at.desc())
        .limit(20)
        .all()
    )
    return [
        {"id": str(c.id), "title": c.title, "updated_at": c.updated_at.isoformat()}
        for c in convs
    ]
