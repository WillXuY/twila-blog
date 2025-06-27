import uuid

from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID

from application.extensions import db
from .base import BaseModel

class Message(BaseModel):
    __tablename__ = 'messages'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    conversation_id = db.Column(UUID(as_uuid=True), db.ForeignKey('twila_app.conversations.id', ondelete='CASCADE'), nullable=False)
    role = db.Column(db.Enum('user', 'assistant', name='role_enum'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)
