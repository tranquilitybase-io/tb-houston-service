from sqlalchemy.ext.declarative import declarative_base
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from config import db

Base = declarative_base()

class NotificationTeam(Base):
    __tablename__ = "notificationTeam"
    isActive = db.Column(db.Boolean())
    lastUpdated = db.Column(db.String(20))
    notificationId = db.Column(db.Integer(), db.ForeignKey("notification.id"), primary_key=True)
    teamId = db.Column(db.Integer(), db.ForeignKey("team.id"), primary_key=True)

    def __repr__(self):
        return "<NotificationTeam(notificationId={self.notificationId!r}, teamId={self.teamId!r})>".format(self=self)

class NotificationTeamSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = NotificationTeam
        include_fk = True
        load_instance = True
