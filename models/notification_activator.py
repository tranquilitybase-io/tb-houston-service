from sqlalchemy.ext.declarative import declarative_base
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from config import db

Base = declarative_base()

class NotificationActivator(Base):
    __tablename__ = "notificationActivator"
    isActive = db.Column(db.Boolean())
    lastUpdated = db.Column(db.String(20))
    notificationId = db.Column(
        db.Integer(), db.ForeignKey("notification.id"), primary_key=True
    )
    activatorId = db.Column(
        db.Integer(), db.ForeignKey("activator.id"), primary_key=True
    )

    def __repr__(self):
        return "<NotificationActivator(notificationId={self.notificationId!r}, activatorId={self.activatorId!r})>".format(self=self)

class NotificationActivatorSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = NotificationActivator
        include_fk = True
        load_instance = True
