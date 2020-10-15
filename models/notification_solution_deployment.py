from sqlalchemy.ext.declarative import declarative_base
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from config import db

Base = declarative_base()

class NotificationSolutionDeployment(Base):
    __tablename__ = "notificationSolutionDeployment"
    isActive = db.Column(db.Boolean())
    lastUpdated = db.Column(db.String(20))
    notificationId = db.Column(db.Integer(), db.ForeignKey("notification.id"), primary_key=True)
    solutionId = db.Column(db.Integer(), db.ForeignKey("solution.id"), primary_key=True)

    def __repr__(self):
        return "<NotificationSolutionDeployment(notificationId={self.notificationId!r}, solutionId={self.solutionId!r})>".format(self=self)

class NotificationSolutionDeploymentSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = NotificationSolutionDeployment
        include_fk = True
        load_instance = True
