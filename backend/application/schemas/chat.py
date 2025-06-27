from marshmallow import Schema, fields
from marshmallow.validate import Length


class ChatRequestSchema(Schema):
    user_id = fields.UUID(required=True)
    conversation_id = fields.UUID(allow_none=True)
    message = fields.Str(required=True, validate=Length(min=1))


class ConversationSchema(Schema):
    id = fields.UUID()
    title = fields.Str()
    user_id = fields.UUID()
    created_at = fields.DateTime()


class MessageSchema(Schema):
    id = fields.UUID()
    conversation_id = fields.UUID()
    role = fields.Str()
    content = fields.Str()
    created_at = fields.DateTime()
