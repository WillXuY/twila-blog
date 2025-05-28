from application.extensions import db

class BaseModel(db.Model):
    __abstract__ = True
    __table_args__ = {'schema': 'twila_app'}
