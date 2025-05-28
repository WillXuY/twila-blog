import uuid

from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID

from application.extensions import db
from .base import BaseModel

class Conversation(BaseModel):
    __tablename__ = 'conversations'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = db.Column(db.Text, default='New Chat')
    user_id = db.Column(UUID(as_uuid=True), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)
    updated_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

    messages = db.relationship("Message", backref="conversation", cascade="all, delete-orphan", passive_deletes=True)
