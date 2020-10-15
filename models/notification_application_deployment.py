from sqlalchemy.ext.declarative import declarative_base
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from config import db

Base = declarative_base()

class NotificationApplicationDeployment(Base):
    __tablename__ = "notificationApplicationDeployment"
    isActive = db.Column(db.Boolean())
    lastUpdated = db.Column(db.String(20))
    notificationId = db.Column(db.Integer(), db.ForeignKey("notification.id"), primary_key=True)
    applicationId = db.Column(db.Integer(), db.ForeignKey("application.id"), primary_key=True)

    def __repr__(self):
        return "<NotificationApplicationDeployment(notificationId={self.notificationId!r}, applicationId={self.applicationId!r})>".format(self=self)

class NotificationApplicationDeploymentSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = NotificationApplicationDeployment
        include_fk = True
        load_instance = True
