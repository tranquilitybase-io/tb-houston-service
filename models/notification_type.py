from sqlalchemy.ext.declarative import declarative_base
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from config import db

Base = declarative_base()

class NotificationType(Base):
    __tablename__ = "notificationType"
    id = db.Column(db.Integer, primary_key=True)
    isActive = db.Column(db.Boolean)
    lastUpdated = db.Column(db.String(20))
    name = db.Column(db.String(45))

    def __repr__(self):
        return "<NotificationType(id={self.id!r})>".format(self=self)

class NotificationTypeSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = NotificationType
        include_fk = True
        load_instance = True
