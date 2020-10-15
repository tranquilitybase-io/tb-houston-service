from sqlalchemy.ext.declarative import declarative_base
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from config import db

Base = declarative_base()

class Notification(Base):
    __tablename__ = "notification"
    id = db.Column(db.Integer(), primary_key=True)
    isActive = db.Column(db.Boolean())
    lastUpdated = db.Column(db.String(20))
    toUserId = db.Column(db.Integer(), db.ForeignKey("user.id"))
    fromUserId = db.Column(db.Integer, db.ForeignKey("user.id"))
    importance = db.Column(db.Integer())
    message = db.Column(db.String(255))
    isRead = db.Column(db.Boolean())
    typeId = db.Column(db.Integer(), db.ForeignKey("notificationType.id"))

    def __repr__(self):
        return "<Notification(id={self.id!r})>".format(self=self)

class NotificationSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Notification
        include_fk = True
        load_instance = True
